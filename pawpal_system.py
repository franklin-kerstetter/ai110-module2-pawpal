from abc import ABC, abstractmethod
from datetime import time, timedelta, date
from enum import Enum
from typing import List


class PetClassification(Enum):
    DOG = 0
    CAT = 1
    BIRD = 2
    SMALL_MAMMAL = 3


class Owner:
    def __init__(self, name: str, available_hours_start: time, available_hours_end: time):
        self._name = name
        self._available_hours_start = available_hours_start
        self._available_hours_end = available_hours_end

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_available_hours_start(self) -> time:
        return self._available_hours_start

    def set_available_hours_start(self, available_hours_start: time) -> None:
        self._available_hours_start = available_hours_start

    def get_available_hours_end(self) -> time:
        return self._available_hours_end

    def set_available_hours_end(self, available_hours_end: time) -> None:
        self._available_hours_end = available_hours_end


class RecurrencePattern(ABC):
    pass


class DailyPattern(RecurrencePattern):
    pass


class WeeklyPattern(RecurrencePattern):
    def __init__(self, days: List[int]):
        self._days = days

    def get_days(self) -> List[int]:
        return self._days

    def set_days(self, days: List[int]) -> None:
        self._days = days


class MonthlyPattern(RecurrencePattern):
    def __init__(self, day_of_month: List[int]):
        self._day_of_month = day_of_month

    def get_day_of_month(self) -> List[int]:
        return self._day_of_month

    def set_day_of_month(self, day_of_month: List[int]) -> None:
        self._day_of_month = day_of_month


class Task:
    def __init__(self, name: str, duration: timedelta, priority: int, recurrence_pattern: RecurrencePattern):
        self._name = name
        self._duration = duration
        self._priority = priority
        self._recurrence_pattern = recurrence_pattern
        self._preceding_tasks: List[Task] = []

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_duration(self) -> timedelta:
        return self._duration

    def set_duration(self, duration: timedelta) -> None:
        self._duration = duration

    def get_priority(self) -> int:
        return self._priority

    def set_priority(self, priority: int) -> None:
        self._priority = priority

    def get_recurrence_pattern(self) -> RecurrencePattern:
        return self._recurrence_pattern

    def set_recurrence_pattern(self, recurrence_pattern: RecurrencePattern) -> None:
        self._recurrence_pattern = recurrence_pattern

    def get_preceding_tasks(self) -> List['Task']:
        return self._preceding_tasks

    def add_preceding_task(self, task: 'Task') -> None:
        self._preceding_tasks.append(task)

    def is_necessary_for_date(self, target_date: date) -> bool:
        pass


class Pet:
    def __init__(self, name: str, classification: PetClassification):
        self._name = name
        self._classification = classification
        self._tasks: List[Task] = []

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_classification(self) -> PetClassification:
        return self._classification

    def set_classification(self, classification: PetClassification) -> None:
        self._classification = classification

    def get_tasks(self) -> List[Task]:
        return self._tasks

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def get_prioritized_tasks_for_date(self, target_date: date) -> List[Task]:
        pass


class ScheduleBlock(ABC):
    def __init__(self, start_time: time, comment: str = ""):
        self._start_time = start_time
        self._comment = comment

    def get_start_time(self) -> time:
        return self._start_time

    def set_start_time(self, start_time: time) -> None:
        self._start_time = start_time

    def get_comment(self) -> str:
        return self._comment

    def set_comment(self, comment: str) -> None:
        self._comment = comment

    @abstractmethod
    def get_timedelta(self) -> timedelta:
        pass

    @abstractmethod
    def is_completed(self) -> bool:
        pass


class OwnerScheduleBlock(ScheduleBlock):
    def __init__(self, start_time: time, duration: timedelta, comment: str = ""):
        super().__init__(start_time, comment)
        self._duration = duration

    def get_duration(self) -> timedelta:
        return self._duration

    def set_duration(self, duration: timedelta) -> None:
        self._duration = duration

    def get_timedelta(self) -> timedelta:
        return self._duration

    def is_completed(self) -> bool:
        pass


class TaskScheduleBlock(ScheduleBlock):
    def __init__(self, start_time: time, task: Task, completed: bool = False, comment: str = ""):
        super().__init__(start_time, comment)
        self._task = task
        self._completed = completed

    def get_task(self) -> Task:
        return self._task

    def set_task(self, task: Task) -> None:
        self._task = task

    def get_completed(self) -> bool:
        return self._completed

    def set_completed(self, completed: bool) -> None:
        self._completed = completed

    def get_timedelta(self) -> timedelta:
        return self._task.get_duration()

    def is_completed(self) -> bool:
        return self._completed


class Schedule:
    def __init__(self, date: date, explanation: str = ""):
        self._date = date
        self._explanation = explanation
        self._blocks: List[ScheduleBlock] = []

    def get_date(self) -> date:
        return self._date

    def set_date(self, date: date) -> None:
        self._date = date

    def get_explanation(self) -> str:
        return self._explanation

    def set_explanation(self, explanation: str) -> None:
        self._explanation = explanation

    def get_blocks(self) -> List[ScheduleBlock]:
        return self._blocks

    def add_block(self, block: ScheduleBlock) -> None:
        self._blocks.append(block)


class Scheduler:
    """Singleton factory. Single scheduler instance manages all schedules.
    Access via Scheduler() or Scheduler.get_instance() — both return same instance."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'Scheduler':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate_schedule(self, owner: Owner, target_date: date) -> Schedule:
        pass