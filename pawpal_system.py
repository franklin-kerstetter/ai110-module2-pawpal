from abc import ABC, abstractmethod
from datetime import time, timedelta, date, datetime
from enum import Enum
from typing import List, Dict, Optional


class PetClassification(Enum):
    DOG = 0
    CAT = 1
    BIRD = 2
    SMALL_MAMMAL = 3

class TimeOfDay(Enum):
    MORNING = 0
    MIDDAY = 1
    EVENING = 2
    NIGHT = 3


class Owner:
    def __init__(self, name: str, available_hours_start: time, available_hours_end: time):
        self._name = name
        self._available_hours_start = available_hours_start
        self._available_hours_end = available_hours_end
        self._pets: List['Pet'] = []
        self._schedules: Dict[date, 'Schedule'] = {}

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

    def get_pets(self) -> List['Pet']:
        return self._pets

    def add_pet(self, pet: 'Pet') -> None:
        self._pets.append(pet)

    def get_schedules(self) -> Dict[date, 'Schedule']:
        return self._schedules

    def get_schedule(self, target_date: date) -> Optional['Schedule']:
        return self._schedules.get(target_date)

    def add_schedule(self, schedule: 'Schedule') -> None:
        self._schedules[schedule.get_date()] = schedule


class RecurrencePattern(ABC):
    @abstractmethod
    def applies_to_date(self, target_date: date) -> bool:
        pass


class DailyPattern(RecurrencePattern):
    def applies_to_date(self, target_date: date) -> bool:
        return True


class WeeklyPattern(RecurrencePattern):
    def __init__(self, days: List[int]):
        self._days = days

    def get_days(self) -> List[int]:
        return self._days

    def set_days(self, days: List[int]) -> None:
        self._days = days

    def applies_to_date(self, target_date: date) -> bool:
        return target_date.weekday() in self._days


class MonthlyPattern(RecurrencePattern):
    def __init__(self, day_of_month: List[int]):
        self._day_of_month = day_of_month

    def get_day_of_month(self) -> List[int]:
        return self._day_of_month

    def set_day_of_month(self, day_of_month: List[int]) -> None:
        self._day_of_month = day_of_month

    def applies_to_date(self, target_date: date) -> bool:
        return target_date.day in self._day_of_month


class Task:
    def __init__(self, name: str, duration: timedelta, priority: int, recurrence_pattern: RecurrencePattern, time_of_day: TimeOfDay):
        self._name = name
        self._duration = duration
        self._priority = priority
        self._recurrence_pattern = recurrence_pattern
        self._time_of_day = time_of_day
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

    def get_time_of_day(self) -> TimeOfDay:
        return self._time_of_day

    def set_time_of_day(self, time_of_day: TimeOfDay) -> None:
        self._time_of_day = time_of_day

    def get_preceding_tasks(self) -> List['Task']:
        return self._preceding_tasks

    def add_preceding_task(self, task: 'Task') -> None:
        self._preceding_tasks.append(task)

    def is_necessary_for_date(self, target_date: date) -> bool:
        return self._recurrence_pattern.applies_to_date(target_date)


class Pet:
    def __init__(self, name: str, classification: PetClassification, age: int = 0, birthday: Optional[date] = None):
        self._name = name
        self._classification = classification
        self._age = age
        self._birthday = birthday if birthday is not None else date.today()
        self._tasks: List[Task] = []

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_classification(self) -> PetClassification:
        return self._classification

    def set_classification(self, classification: PetClassification) -> None:
        self._classification = classification

    def get_age(self) -> int:
        return self._age

    def set_age(self, age: int) -> None:
        self._age = age

    def get_birthday(self) -> date:
        return self._birthday

    def set_birthday(self, birthday: date) -> None:
        self._birthday = birthday

    def get_tasks(self) -> List[Task]:
        return self._tasks

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def get_prioritized_tasks_for_date(self, target_date: date) -> List[Task]:
        pass


class ScheduleBlock(ABC):
    def __init__(self, start_time: datetime, comment: str = ""):
        self._start_time = start_time
        self._comment = comment

    def get_start_time(self) -> datetime:
        return self._start_time

    def set_start_time(self, start_time: datetime) -> None:
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
    def __init__(self, start_time: datetime, duration: timedelta, comment: str = ""):
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
    def __init__(self, start_time: datetime, task: Task, completed: bool = False, comment: str = ""):
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
    _tasks_by_time_of_day: Dict[TimeOfDay, time] = {
        TimeOfDay.MORNING: time(hour=5, min=0),
        TimeOfDay.MIDDAY: time(hour=11, min=0),
        TimeOfDay.EVENING: time(hour=17, min=0),
        TimeOfDay.NIGHT: time(hour=23, min=0)
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'Scheduler':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_task_pet_tuples_by_time_of_day_for_owner(self, owner: Owner, target_date: date) -> Dict[TimeOfDay, List[tuple[Task, Pet]]]:
        # Initialize dictionary with empty lists for each time of day
        tasks_by_time_of_day: Dict[TimeOfDay, List[tuple[Task, Pet]]] = {
            time_of_day: [] for time_of_day in TimeOfDay
        }

        # Collect applicable tasks from each pet and group by the task's time of day
        for pet in owner.get_pets():
            for task in pet.get_tasks():
                if task.is_necessary_for_date(target_date):
                    tasks_by_time_of_day[task.get_time_of_day()].append((task, pet))

        # Sort tasks within each time of day group by priority (higher first)
        # and by pet age (older pets first) as a tiebreaker
        for time_of_day in TimeOfDay:
            tasks_by_time_of_day[time_of_day].sort(
                key=lambda x: (x[0].get_priority(), x[1].get_age()),
                reverse=True
            )

        return tasks_by_time_of_day

    def generate_schedule(self, owner: Owner, target_date: date) -> Schedule:
        schedule = Schedule(target_date)

        # Get applicable tasks grouped by time of day and sorted by priority + pet age
        tasks_by_time = self.get_task_pet_tuples_by_time_of_day_for_owner(owner, target_date)

        # Collect all applicable tasks for tracking
        applicable_tasks: List[tuple[Task, Pet]] = []
        for task_list in tasks_by_time.values():
            applicable_tasks.extend(task_list)

        # Track which tasks were actually scheduled
        scheduled_tasks: set[tuple[Task, Pet]] = set()

        # Start at earliest of MORNING or owner's availability
        start_datetime = max(
            datetime.combine(target_date, self._tasks_by_time_of_day[TimeOfDay.MORNING]),
            datetime.combine(target_date, owner.get_available_hours_start())
        )
        current_datetime = start_datetime

        # Process each time period in order
        time_periods = list(TimeOfDay)

        for i, time_period in enumerate(time_periods):
            tasks = tasks_by_time[time_period]
            period_start_datetime = datetime.combine(target_date, self._tasks_by_time_of_day[time_period])

            # Use current time if already past period start, otherwise jump to period start
            if current_datetime < period_start_datetime:
                current_datetime = period_start_datetime

            # Determine boundary for this period (next period's start time)
            if i < len(time_periods) - 1:
                next_period_start = datetime.combine(target_date, self._tasks_by_time_of_day[time_periods[i + 1]])
            else:
                next_period_start = datetime.combine(target_date, time(23, 59))

            # Process each task in this time period
            for task, pet in tasks:
                # Stop if we've reached or passed next period
                if current_datetime >= next_period_start:
                    break

                block = TaskScheduleBlock(current_datetime, task)
                schedule.add_block(block)
                scheduled_tasks.add((task, pet))

                # Increment current datetime by task duration
                current_datetime = current_datetime + task.get_duration()

        # Build explanation with pets, scheduling status, and missing tasks if any
        missing_tasks = [(task, pet) for task, pet in applicable_tasks if (task, pet) not in scheduled_tasks]

        if missing_tasks:
            scheduled_count = len(scheduled_tasks)
            total_count = len(applicable_tasks)
            missing_details = "; ".join([f"{task.get_name()} ({pet.get_name()})" for task, pet in missing_tasks])
            explanation = f"Scheduled {scheduled_count}/{total_count} tasks. Missing: {missing_details}."
        else:
            pet_names = [pet.get_name() for pet in owner.get_pets()]
            pets_text = ", ".join(pet_names) if pet_names else "no pets"
            explanation = f"Pets: {pets_text}. All tasks scheduled."

        schedule.set_explanation(explanation)

        owner.add_schedule(schedule)
        return schedule