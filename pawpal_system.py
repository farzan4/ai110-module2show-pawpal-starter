"""Core data models and scheduling interfaces for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time
from typing import Dict, List, Optional


@dataclass
class Task:
	"""A pet-care task and its scheduling preferences."""

	task_id: str
	title: str
	category: str
	duration_mins: int
	priority: int
	preferred_time: Optional[time] = None
	is_flexible: bool = True
	is_completed: bool = False

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		raise NotImplementedError

	def update_details(self, **changes: object) -> None:
		"""Update task details; validation will be added with the behavior."""
		raise NotImplementedError


@dataclass
class Pet:
	"""A pet profile and the tasks associated with that pet."""

	pet_id: str
	name: str
	species: str
	age: float
	special_needs: List[str] = field(default_factory=list)
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a care task to this pet."""
		raise NotImplementedError

	def remove_task(self, task_id: str) -> None:
		"""Remove a task by its ID."""
		raise NotImplementedError

	def get_pending_tasks(self) -> List[Task]:
		"""Return this pet's tasks that are not yet completed."""
		raise NotImplementedError


@dataclass
class Owner:
	"""An owner, their pets, and their planning preferences."""

	owner_id: str
	name: str
	daily_available_mins: int
	pets: List[Pet] = field(default_factory=list)
	preferences: Dict[str, object] = field(default_factory=dict)

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner's profile."""
		raise NotImplementedError

	def get_all_tasks(self) -> List[Task]:
		"""Return tasks belonging to all of this owner's pets."""
		raise NotImplementedError


@dataclass
class TimeSlot:
	"""A task assigned a start and end time."""

	task: Task
	start_time: time
	end_time: time

	def overlaps_with(self, other: TimeSlot) -> bool:
		"""Return whether this slot overlaps another slot."""
		raise NotImplementedError

	def get_duration_minutes(self) -> int:
		"""Return the length of this slot in minutes."""
		raise NotImplementedError


class Scheduler:
	"""Scheduling interface; conflict resolution will be implemented later."""

	def generate_schedule(
		self, tasks: List[Task], available_mins: int
	) -> DailyPlan:
		"""Build a daily plan from tasks and the available time budget."""
		raise NotImplementedError

	def _resolve_conflicts(self, slots: List[TimeSlot]) -> List[TimeSlot]:
		"""Resolve overlapping slots in a proposed schedule."""
		raise NotImplementedError


@dataclass
class DailyPlan:
	"""The scheduled and omitted tasks for one day."""

	plan_date: date = field(default_factory=date.today)
	scheduled_slots: List[TimeSlot] = field(default_factory=list)
	omitted_tasks: List[Task] = field(default_factory=list)
	reasoning_log: List[str] = field(default_factory=list)

	def get_total_scheduled_minutes(self) -> int:
		"""Return the total duration of all scheduled slots."""
		raise NotImplementedError

	def get_plan_summary(self) -> str:
		"""Return a human-readable summary of the plan."""
		raise NotImplementedError
