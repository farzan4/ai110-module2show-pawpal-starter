from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
	task = Task("task-1", "Feed dog", "feeding", 10, 1)

	task.mark_complete()

	assert task.is_completed is True


def test_adding_task_increases_pet_task_count():
	pet = Pet("pet-1", "Buddy", "dog", 3)
	task = Task("task-1", "Feed dog", "feeding", 10, 1)
	initial_task_count = len(pet.tasks)

	pet.add_task(task)

	assert len(pet.tasks) == initial_task_count + 1
