from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status():
	task = Task("task-1", "Feed dog", "feeding", 10, 1)

	task.mark_complete()

	assert task.is_completed is True


def test_completing_daily_task_adds_next_occurrence_for_tomorrow():
	pet = Pet("pet-1", "Buddy", "dog", 3)
	task = Task(
		"task-1", "Feed dog", "feeding", 10, 1,
		frequency="Daily", scheduled_time=time(8, 30)
	)
	pet.add_task(task)

	pet.mark_task_complete(task.task_id)

	assert task.is_completed is True
	assert len(pet.tasks) == 2
	next_task = pet.tasks[1]
	assert next_task is not task
	assert next_task.task_id != task.task_id
	assert next_task.is_completed is False
	assert next_task.frequency == "Daily"
	assert next_task.due_date == date.today() + timedelta(days=1)
	assert next_task.scheduled_time == time(8, 30)


def test_completing_weekly_task_adds_next_occurrence_in_seven_days():
	pet = Pet("pet-1", "Buddy", "dog", 3)
	task = Task("task-1", "Groom dog", "grooming", 30, 2, frequency="weekly")
	pet.add_task(task)

	pet.mark_task_complete(task.task_id)

	assert len(pet.tasks) == 2
	assert pet.tasks[1].due_date == date.today() + timedelta(days=7)


def test_completing_one_time_task_does_not_add_another_task():
	pet = Pet("pet-1", "Buddy", "dog", 3)
	task = Task("task-1", "Feed dog", "feeding", 10, 1)
	pet.add_task(task)

	pet.mark_task_complete(task.task_id)

	assert task.is_completed is True
	assert pet.tasks == [task]


def test_adding_task_increases_pet_task_count():
	pet = Pet("pet-1", "Buddy", "dog", 3)
	task = Task("task-1", "Feed dog", "feeding", 10, 1)
	initial_task_count = len(pet.tasks)

	pet.add_task(task)

	assert len(pet.tasks) == initial_task_count + 1


def test_sort_by_time_orders_tasks_by_duration_without_mutating_input():
	tasks = [
		Task("task-1", "Long walk", "exercise", 30, 2),
		Task("task-2", "Feed dog", "feeding", 10, 1),
		Task("task-3", "Medication", "health", 5, 1),
	]

	scheduler = Scheduler()
	sorted_tasks = scheduler.sort_by_duration(tasks)

	assert [task.duration_mins for task in sorted_tasks] == [5, 10, 30]
	assert tasks[0].duration_mins == 30
	assert scheduler.sort_by_time(tasks) == sorted_tasks


def test_scheduler_skips_oversized_task_and_schedules_later_shorter_task():
	tasks = [
		Task("task-1", "Long walk", "exercise", 30, 1),
		Task("task-2", "Grooming", "grooming", 40, 2),
		Task("task-3", "Medication", "health", 5, 3),
	]

	scheduled, omitted, _ = Scheduler().generate_schedule(tasks, 35)

	assert [task.title for task in scheduled] == ["Long walk", "Medication"]
	assert [task.title for task in omitted] == ["Grooming"]


def test_scheduler_does_not_warn_for_tasks_that_start_at_previous_end():
	tasks = [
		Task("task-1", "Walk Buddy", "exercise", 30, 1, scheduled_time=time(9, 0)),
		Task("task-2", "Feed Buddy", "feeding", 10, 2, scheduled_time=time(9, 30)),
	]

	_, _, reasoning = Scheduler().generate_schedule(tasks, 60)

	assert not any("Warning:" in message for message in reasoning)


def test_scheduler_warns_when_same_pet_tasks_overlap():
	pet = Pet("pet-1", "Buddy", "dog", 3)
	pet.add_task(
		Task("task-1", "Walk Buddy", "exercise", 30, 1, scheduled_time=time(9, 0))
	)
	pet.add_task(
		Task("task-2", "Feed Buddy", "feeding", 10, 2, scheduled_time=time(9, 15))
	)

	scheduled, omitted, reasoning = Scheduler().generate_schedule(pet.get_pending_tasks(), 60)

	assert len(scheduled) == 2
	assert omitted == []
	assert any(
		"Warning:" in message and "Walk Buddy" in message and "Feed Buddy" in message
		for message in reasoning
	)


def test_scheduler_warns_when_different_pets_tasks_start_together():
	buddy = Pet("pet-1", "Buddy", "dog", 3)
	luna = Pet("pet-2", "Luna", "cat", 2)
	buddy.add_task(
		Task("task-1", "Walk Buddy", "exercise", 30, 1, scheduled_time=time(9, 0))
	)
	luna.add_task(
		Task("task-2", "Feed Luna", "feeding", 10, 2, scheduled_time=time(9, 0))
	)

	scheduled, omitted, reasoning = Scheduler().generate_schedule(
		buddy.get_pending_tasks() + luna.get_pending_tasks(), 60
	)

	assert len(scheduled) == 2
	assert omitted == []
	assert any("Warning:" in message and "09:00" in message for message in reasoning)


def test_owner_filter_tasks_by_completion_status_and_pet_name():
	owner = Owner("owner-1", "Jordan", 60)
	buddy = Pet("pet-1", "Buddy", "dog", 3)
	luna = Pet("pet-2", "Luna", "cat", 2)
	completed_task = Task("task-1", "Feed Buddy", "feeding", 10, 1)
	pending_task = Task("task-2", "Walk Buddy", "exercise", 20, 2)
	luna_task = Task("task-3", "Feed Luna", "feeding", 10, 1)
	completed_task.mark_complete()
	buddy.add_task(completed_task)
	buddy.add_task(pending_task)
	luna.add_task(luna_task)
	owner.add_pet(buddy)
	owner.add_pet(luna)

	assert owner.filter_tasks(is_completed=True, pet_name="buddy") == [completed_task]
	assert owner.filter_tasks(is_completed=False, pet_name="Luna") == [luna_task]
	assert owner.filter_tasks(pet_name="unknown") == []


def test_tasks_are_returned_in_chronological_order():
	tasks = [
		Task(
			"task-3",
			"Evening walk",
			"exercise",
			20,
			2,
			due_date=date(2026, 10, 18),
			scheduled_time=time(18, 0),
		),
		Task(
			"task-1",
			"Morning meds",
			"health",
			10,
			1,
			due_date=date(2026, 10, 18),
			scheduled_time=time(8, 30),
		),
		Task(
			"task-2",
			"Lunch walk",
			"exercise",
			15,
			2,
			due_date=date(2026, 10, 18),
			scheduled_time=time(12, 0),
		),
	]

	ordered = sorted(tasks, key=lambda task: (task.due_date, task.scheduled_time or time.min))

	assert [task.task_id for task in ordered] == ["task-1", "task-2", "task-3"]


def test_marking_daily_task_complete_creates_next_day_occurrence():
	task = Task(
		"task-1",
		"Feed dog",
		"feeding",
		10,
		1,
		frequency="daily",
		scheduled_time=time(8, 0),
	)

	next_task = task.mark_complete()

	assert task.is_completed is True
	assert next_task is not None
	assert next_task.is_completed is False
	assert next_task.frequency == "daily"
	assert next_task.due_date == date.today() + timedelta(days=1)
	assert next_task.scheduled_time == time(8, 0)


def test_scheduler_flags_duplicate_times_as_conflicts():
	tasks = [
		Task(
			"task-1",
			"Walk Buddy",
			"exercise",
			30,
			1,
			due_date=date(2026, 10, 18),
			scheduled_time=time(9, 0),
		),
		Task(
			"task-2",
			"Feed Buddy",
			"feeding",
			10,
			2,
			due_date=date(2026, 10, 18),
			scheduled_time=time(9, 0),
		),
	]

	warnings = Scheduler()._get_overlap_warnings(tasks)

	assert len(warnings) == 1
	assert "Walk Buddy" in warnings[0]
	assert "Feed Buddy" in warnings[0]
