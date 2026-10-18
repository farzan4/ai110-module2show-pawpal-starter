# main.py
from datetime import time

from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # 1. Create an Owner with a 60-minute daily budget
    owner = Owner(
        owner_id="o1",
        name="Alex",
        daily_available_mins=60
    )

    # 2. Create two Pets
    dog = Pet(pet_id="p1", name="Luna", species="Dog", age=3.0, special_needs=["Hip Dysplasia"])
    cat = Pet(pet_id="p2", name="Milo", species="Cat", age=2.0)

    owner.add_pet(dog)
    owner.add_pet(cat)

    # 3. Add Tasks with varying durations and priorities, deliberately out of order
    # Note: Priority 1 is highest priority
    task1 = Task(task_id="t1", title="Give Luna Joint Supplement", category="Health", duration_mins=5, priority=1, scheduled_time=time(9, 0))
    task2 = Task(task_id="t2", title="Luna Neighborhood Walk", category="Exercise", duration_mins=30, priority=2, scheduled_time=time(9, 0))
    task3 = Task(task_id="t3", title="Groom Milo's Fur", category="Grooming", duration_mins=15, priority=3)
    task4 = Task(task_id="t4", title="Extended Dog Park Play", category="Enrichment", duration_mins=25, priority=4)
    completed_task = Task(task_id="t5", title="Milo's Morning Feeding", category="Feeding", duration_mins=10, priority=1)
    completed_task.mark_complete()

    dog.add_task(task4)
    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)
    cat.add_task(completed_task)

    # 4. Collect all tasks across pets and generate schedule
    all_tasks = owner.get_all_tasks()
    scheduler = Scheduler()

    print("\n🔀 TASKS SORTED BY DURATION:")
    for t in scheduler.sort_by_time(all_tasks):
        print(f"  • [{t.category}] {t.title} ({t.duration_mins}m)")

    print(f"\n🔎 FILTERED TASKS (Pending, {dog.name}):")
    filtered_tasks = owner.filter_tasks(is_completed=False, pet_name=dog.name)
    for t in filtered_tasks:
        print(f"  • [{t.category}] {t.title} ({t.duration_mins}m)")
    if not filtered_tasks:
        print("  None.")

    print(f"\n✅ FILTERED TASKS (Completed, {cat.name}):")
    completed_tasks = owner.filter_tasks(is_completed=True, pet_name=cat.name)
    for t in completed_tasks:
        print(f"  • [{t.category}] {t.title} ({t.duration_mins}m)")
    if not completed_tasks:
        print("  None.")

    scheduled, omitted, reasoning = scheduler.generate_schedule(
        tasks=all_tasks, 
        available_mins=owner.daily_available_mins
    )

    # 5. Print "Today's Schedule" to terminal
    print("=" * 45)
    print(f"       PAWPAL+ DAILY SCHEDULE FOR {owner.name.upper()}")
    print(f"   Daily Time Budget: {owner.daily_available_mins} minutes")
    print("=" * 45)

    print("\n✅ SCHEDULED TASKS:")
    total_time = 0
    if scheduled:
        for t in scheduled:
            scheduled_time = (
                f" at {t.scheduled_time.strftime('%H:%M')}"
                if t.scheduled_time is not None
                else ""
            )
            print(f"  • [{t.category}] {t.title} ({t.duration_mins}m){scheduled_time} - Priority {t.priority}")
            total_time += t.duration_mins
        print(f"\nTotal Scheduled Time: {total_time} / {owner.daily_available_mins} mins")
    else:
        print("  No tasks scheduled.")

    print("\n⚠️ OMITTED TASKS (Over Budget):")
    if omitted:
        for t in omitted:
            print(f"  • [{t.category}] {t.title} ({t.duration_mins}m) - Priority {t.priority}")
    else:
        print("  None! All tasks fit into your daily schedule.")

    print("\n📋 SCHEDULER LOG / REASONING:")
    for log_entry in reasoning:
        if log_entry.startswith("Warning:"):
            print(f"  ⚠️ {log_entry}")
        else:
            print(f"  - {log_entry}")
    print("=" * 45)

if __name__ == "__main__":
    main()