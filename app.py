from datetime import time
from uuid import uuid4

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(
        owner_id="owner-1",
        name="Jordan",
        daily_available_mins=120,
    )

owner: Owner = st.session_state["owner"]
owner.name = st.text_input("Owner name", value=owner.name)
owner.daily_available_mins = st.number_input(
    "Daily time available (minutes)",
    min_value=1,
    max_value=1440,
    value=owner.daily_available_mins,
)

st.divider()
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    col1, col2 = st.columns(2)
    with col1:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col2:
        pet_age = st.number_input("Age (years)", min_value=0.0, max_value=100.0, value=1.0)
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    pet = Pet(
        pet_id=str(uuid4()),
        name=pet_name.strip(),
        species=species,
        age=float(pet_age),
    )
    if pet.name:
        owner.add_pet(pet)
        st.success(f"Added {pet.name} to {owner.name}'s pets.")
    else:
        st.error("Enter a name for the pet.")

if owner.pets:
    st.write("Your pets:", ", ".join(f"{pet.name} ({pet.species})" for pet in owner.pets))
else:
    st.info("Add a pet before creating care tasks.")

st.divider()
st.subheader("Schedule a Task")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        pet_index = st.selectbox(
            "Pet", options=range(len(owner.pets)), format_func=lambda index: owner.pets[index].name
        )
        task_title = st.text_input("Task title", value="Morning walk")
        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.selectbox("Category", ["Feeding", "Exercise", "Health", "Grooming", "Enrichment", "Other"])
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority_label = st.selectbox("Priority", ["high", "medium", "low"])
        scheduled_time = st.time_input("Scheduled time", value=time(9, 0))
        frequency = st.selectbox("Repeat", ["Once", "Daily", "Weekly"])
        add_task = st.form_submit_button("Add task")

    if add_task:
        title = task_title.strip()
        if title:
            priority = {"high": 1, "medium": 2, "low": 3}[priority_label]
            task = Task(
                task_id=str(uuid4()),
                title=title,
                category=category,
                duration_mins=int(duration),
                priority=priority,
                frequency=frequency,
                scheduled_time=scheduled_time,
            )
            owner.pets[pet_index].add_task(task)
            st.success(f"Added '{task.title}' for {owner.pets[pet_index].name}.")
        else:
            st.error("Enter a title for the task.")

all_tasks = owner.get_all_tasks()
scheduler = Scheduler()
if all_tasks:
    st.markdown("### Pending tasks")
    pet_filter = st.selectbox(
        "Show tasks for",
        ["All pets", *[pet.name for pet in owner.pets]],
        key="pending_task_pet_filter",
    )
    visible_tasks = (
        all_tasks
        if pet_filter == "All pets"
        else owner.filter_tasks(is_completed=False, pet_name=pet_filter)
    )
    sorted_tasks = scheduler.sort_by_duration(visible_tasks)
    st.caption(
        f"Showing {len(sorted_tasks)} pending task(s), sorted by shortest duration."
    )
    pet_names_by_task = {
        id(task): pet.name
        for pet in owner.pets
        for task in pet.get_pending_tasks()
    }
    st.dataframe(
        [
            {
                "Pet": pet_names_by_task[id(task)],
                "Task": task.title,
                "Category": task.category,
                "Duration (min)": task.duration_mins,
                "Priority": {1: "High", 2: "Medium", 3: "Low"}.get(
                    task.priority, str(task.priority)
                ),
                "Frequency": task.frequency.title(),
                "Due date": task.due_date.isoformat(),
                "Scheduled time": (
                    task.scheduled_time.strftime("%H:%M")
                    if task.scheduled_time is not None
                    else "Not set"
                ),
            }
            for task in sorted_tasks
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No pending tasks yet. Add a task above.")

if all_tasks:
    st.markdown("### Mark a task complete")
    for pet in owner.pets:
        for task in pet.get_pending_tasks():
            task_col, button_col = st.columns([4, 1])
            task_col.write(
                f"**{task.title}** — {pet.name}; due {task.due_date.isoformat()}"
            )
            if button_col.button(
                "Complete", key=f"complete-{pet.pet_id}-{task.task_id}"
            ):
                next_task = pet.mark_task_complete(task.task_id)
                st.session_state.pop("schedule_result", None)
                if next_task is not None:
                    st.session_state["completion_message"] = (
                        f"Completed '{task.title}'. Next occurrence due "
                        f"{next_task.due_date.isoformat()}."
                    )
                else:
                    st.session_state["completion_message"] = (
                        f"Completed '{task.title}'."
                    )
                st.rerun()

if "completion_message" in st.session_state:
    st.success(st.session_state.pop("completion_message"))

st.divider()
st.subheader("Build Schedule")
if st.button("Generate schedule", disabled=not all_tasks):
    st.session_state["schedule_result"] = scheduler.generate_schedule(
        tasks=owner.get_all_tasks(),
        available_mins=int(owner.daily_available_mins),
    )

if "schedule_result" in st.session_state:
    scheduled, omitted, reasoning = st.session_state["schedule_result"]
    st.markdown("### Today's plan")
    conflict_warnings = [
        explanation
        for explanation in reasoning
        if explanation.startswith("Warning:")
    ]
    if conflict_warnings:
        conflict_count = len(conflict_warnings)
        st.warning(
            f"{conflict_count} scheduling conflict(s) found. Two care tasks "
            "overlap, so review the task names, date, and start times below. "
            "Adjust a scheduled time or duration to avoid missing or rushing care."
        )
        for warning in conflict_warnings:
            st.markdown(f"- {warning.removeprefix('Warning: ')}")

    if scheduled:
        st.write(f"Scheduled **{sum(task.duration_mins for task in scheduled)} / {int(owner.daily_available_mins)} minutes**")
        for task in scheduled:
            task_time = (
                f" at {task.scheduled_time.strftime('%H:%M')}"
                if task.scheduled_time is not None
                else ""
            )
            st.write(f"✅ **{task.title}** — {task.category}, {task.duration_mins} min{task_time}, priority {task.priority}")
    else:
        st.info("No tasks fit within the available time.")

    if omitted:
        st.markdown("#### Not scheduled")
        for task in omitted:
            st.write(f"⚠️ **{task.title}** — {task.duration_mins} min, priority {task.priority}")

    st.markdown("#### Why this plan")
    for explanation in reasoning:
        if not explanation.startswith("Warning:"):
            st.write(f"- {explanation}")
