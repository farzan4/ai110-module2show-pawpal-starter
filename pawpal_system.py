from dataclasses import dataclass, field
from datetime import date
from typing import List

@dataclass
class Task:
    task_id: str
    title: str
    category: str
    duration_mins: int
    priority: int
    is_completed: bool = False

    def mark_complete(self) -> None:
        pass

    def update_details(self, **kwargs) -> None:
        pass


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    age: float
    special_needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_pending_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    owner_id: str
    name: str
    daily_available_mins: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: str) -> None:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def generate_schedule(self, tasks: List[Task], available_mins: int):
        pass


@dataclass
class DailyPlan:
    plan_date: date
    scheduled_tasks: List[Task] = field(default_factory=list)
    omitted_tasks: List[Task] = field(default_factory=list)
    reasoning_log: List[str] = field(default_factory=list)

    def get_total_scheduled_minutes(self) -> int:
        pass

    def get_plan_summary(self) -> str:
        pass