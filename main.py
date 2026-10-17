# main.py
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

    # 3. Add Tasks with varying durations and priorities
    # Note: Priority 1 is highest priority
    task1 = Task(task_id="t1", title="Give Luna Joint Supplement", category="Health", duration_mins=5, priority=1)
    task2 = Task(task_id="t2", title="Luna Neighborhood Walk", category="Exercise", duration_mins=30, priority=2)
    task3 = Task(task_id="t3", title="Groom Milo's Fur", category="Grooming", duration_mins=15, priority=3)
    task4 = Task(task_id="t4", title="Extended Dog Park Play", category="Enrichment", duration_mins=25, priority=4)

    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task4)
    cat.add_task(task3)

    # 4. Collect all tasks across pets and generate schedule
    all_tasks = owner.get_all_tasks()
    scheduler = Scheduler()
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
            print(f"  • [{t.category}] {t.title} ({t.duration_mins}m) - Priority {t.priority}")
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
        print(f"  - {log_entry}")
    print("=" * 45)

if __name__ == "__main__":
    main()