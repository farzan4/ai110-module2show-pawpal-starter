from dataclasses import dataclass, field
from datetime import date, time, timedelta
from typing import List, Tuple, Any, Optional
from uuid import uuid4

@dataclass
class Task:
    task_id: str
    title: str
    category: str
    duration_mins: int
    priority: int
    is_completed: bool = False
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)
    scheduled_time: Optional[time] = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete and create its next occurrence if recurring.

        Daily and weekly tasks recur from today's date; other frequencies do not
        create another task. An already-completed task is left unchanged.
        Runs in O(1) time and returns the new task, or ``None`` if none is due.
        """
        if self.is_completed:
            return None

        self.is_completed = True
        recurrence_days = {"daily": 1, "weekly": 7}.get(self.frequency.casefold())
        if recurrence_days is None:
            return None

        return Task(
            task_id=str(uuid4()),
            title=self.title,
            category=self.category,
            duration_mins=self.duration_mins,
            priority=self.priority,
            frequency=self.frequency,
            due_date=date.today() + timedelta(days=recurrence_days),
            scheduled_time=self.scheduled_time,
        )

    def update_details(self, **kwargs: Any) -> None:
        """Update existing task attributes from non-None keyword values.

        Unknown attribute names and values of ``None`` are ignored. Runtime is
        O(k) in the number of supplied keyword arguments.
        """
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

    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """Complete the first matching task and append its next occurrence.

        Searches tasks in list order, so this takes O(n) time for n tasks.
        Returns the recurring task's new occurrence, or ``None`` if the ID is
        absent or the matched task does not recur.
        """
        for task in self.tasks:
            if task.task_id == task_id:
                next_task = task.mark_complete()
                if next_task is not None:
                    self.add_task(next_task)
                return next_task
        return None

    def remove_task(self, task_id: str) -> None:
        """Remove every task with the given ID, preserving the others' order.

        This rebuilds the task list in O(n) time for n tasks.
        """
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_pending_tasks(self) -> List[Task]:
        """Return incomplete tasks in their existing order without mutating state.

        The list is filtered in O(n) time for n tasks.
        """
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
        """Remove every pet with the given ID, preserving the others' order.

        This rebuilds the pet list in O(p) time for p pets.
        """
        self.pets = [p for p in self.pets if p.pet_id != pet_id]

    def get_all_tasks(self) -> List[Task]:
        """Collect pending tasks from each pet, preserving pet/task order.

        Runs in O(p + t) time, where p is the pet count and t is the total
        number of tasks across those pets.
        """
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_pending_tasks())
        return all_tasks

    def filter_tasks(
        self,
        is_completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by optional completion state and case-insensitive pet name.

        If either filter is omitted it imposes no restriction. The result keeps
        the original pet and task order; all tasks are scanned in O(p + t) time.
        """
        matching_tasks = []
        for pet in self.pets:
            if pet_name is not None and pet.name.casefold() != pet_name.casefold():
                continue
            matching_tasks.extend(
                task
                for task in pet.tasks
                if is_completed is None or task.is_completed == is_completed
            )
        return matching_tasks


class Scheduler:
    def sort_by_duration(self, tasks: List[Task]) -> List[Task]:
        """Return a new list sorted by duration, shortest first.

        The input order is not modified; sorting takes O(n log n) time.
        """
        return sorted(tasks, key=lambda task: task.duration_mins)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Backward-compatible alias for :meth:`sort_by_duration`.

        Despite this legacy name, the sort key is duration, not clock time.
        """
        return self.sort_by_duration(tasks)

    def _get_overlap_warnings(self, tasks: List[Task]) -> List[str]:
        """Report every overlapping pair of timed tasks on the same due date.

        Tasks are sorted by date and start time, then compared against intervals
        still active at each start. End/start boundaries are non-overlapping.
        Sorting takes O(n log n); dense overlaps can require O(n^2) comparisons
        and produce O(n^2) warnings.
        """
        timed_tasks = [
            (
                task,
                task.scheduled_time.hour * 60 + task.scheduled_time.minute,
            )
            for task in tasks
            if task.scheduled_time is not None
        ]
        timed_tasks.sort(key=lambda item: (item[0].due_date, item[1]))

        warnings: List[str] = []
        active_tasks: List[Tuple[Task, int]] = []
        current_date: Optional[date] = None

        for task, task_start in timed_tasks:
            if task.due_date != current_date:
                active_tasks = []
                current_date = task.due_date

            # An interval ending exactly when this task starts is not an overlap.
            active_tasks = [
                (active_task, task_end)
                for active_task, task_end in active_tasks
                if task_end > task_start
            ]
            for active_task, _ in active_tasks:
                warnings.append(
                    f"Warning: '{active_task.title}' and '{task.title}' overlap "
                    f"on {task.due_date.isoformat()} at "
                    f"{active_task.scheduled_time.strftime('%H:%M')} and "
                    f"{task.scheduled_time.strftime('%H:%M')}."
                )

            active_tasks.append((task, task_start + task.duration_mins))

        return warnings

    def generate_schedule(
        self, tasks: List[Task], available_mins: int
    ) -> Tuple[List[Task], List[Task], List[str]]:
        """Greedily select tasks by priority and report capacity/overlap decisions.

        Tasks are considered by ascending numeric priority, then ascending
        duration. Each task is included if it fits the remaining minutes;
        omitted tasks do not prevent later shorter tasks from being selected.
        This does not backtrack or optimize the number of tasks/minutes used.
        Returns ``(scheduled, omitted, reasoning_log)`` without reordering the
        input list. Selection sorting takes O(n log n); overlap reporting can
        take O(n^2) in the worst case.
        """
        # Sort by priority ascending, then by duration ascending
        sorted_tasks = sorted(tasks, key=lambda t: (t.priority, t.duration_mins))

        scheduled: List[Task] = []
        omitted: List[Task] = []
        reasoning_log: List[str] = []
        remaining_mins = available_mins

        for task in sorted_tasks:
            if task.duration_mins <= remaining_mins:
                scheduled.append(task)
                remaining_mins -= task.duration_mins
                reasoning_log.append(
                    f"Included '{task.title}' ({task.duration_mins}m) - Priority {task.priority}."
                )
            else:
                omitted.append(task)
                reasoning_log.append(
                    f"Omitted '{task.title}' ({task.duration_mins}m) - Exceeds daily limit of {available_mins}m."
                )

        reasoning_log.extend(self._get_overlap_warnings(scheduled))

        return scheduled, omitted, reasoning_log 