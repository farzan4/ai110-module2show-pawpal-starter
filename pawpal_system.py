from dataclasses import dataclass, field
from typing import List, Tuple, Any

@dataclass
class Task:
    task_id: str
    title: str
    category: str
    duration_mins: int
    priority: int
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True

    def update_details(self, **kwargs: Any) -> None:
        """Update task fields when non-None values are provided."""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    age: float
    special_needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the pet by task ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for the pet."""
        return [t for t in self.tasks if not t.is_completed]


@dataclass
class Owner:
    owner_id: str
    name: str
    daily_available_mins: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from the owner's list by pet ID."""
        self.pets = [p for p in self.pets if p.pet_id != pet_id]

    def get_all_tasks(self) -> List[Task]:
        """Return all incomplete tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_pending_tasks())
        return all_tasks


class Scheduler:
    def generate_schedule(
        self, tasks: List[Task], available_mins: int
    ) -> Tuple[List[Task], List[Task], List[str]]:
        """Schedule tasks within the available daily minutes and return the plan."""
        # Sort by priority ascending, then by duration ascending
        sorted_tasks = sorted(tasks, key=lambda t: (t.priority, t.duration_mins))

        scheduled: List[Task] = []
        omitted: List[Task] = []
        reasoning_log: List[str] = []

        current_time_used = 0

        for task in sorted_tasks:
            if current_time_used + task.duration_mins <= available_mins:
                scheduled.append(task)
                current_time_used += task.duration_mins
                reasoning_log.append(
                    f"Included '{task.title}' ({task.duration_mins}m) - Priority {task.priority}."
                )
            else:
                omitted.append(task)
                reasoning_log.append(
                    f"Omitted '{task.title}' ({task.duration_mins}m) - Exceeds daily limit of {available_mins}m."
                )

        return scheduled, omitted, reasoning_log 