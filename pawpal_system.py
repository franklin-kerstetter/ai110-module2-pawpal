from abc import ABC, abstractmethod
from datetime import time, timedelta, date, datetime
from enum import Enum
from typing import List, Dict, Optional
from uuid import uuid4


class PetClassification(Enum):
    DOG = 0
    CAT = 1
    BIRD = 2
    SMALL_MAMMAL = 3
    FISH = 4

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
    def __init__(self, name: str, duration: timedelta, priority: int, recurrence_pattern: RecurrencePattern, time_of_day: TimeOfDay, pet: Optional['Pet'] = None):
        self._name = name
        self._duration = duration
        self._priority = priority
        self._recurrence_pattern = recurrence_pattern
        self._time_of_day = time_of_day
        self._pet = pet
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

    def get_pet(self) -> Optional['Pet']:
        return self._pet

    def set_pet(self, pet: Optional['Pet']) -> None:
        self._pet = pet

    def get_preceding_tasks(self) -> List['Task']:
        return self._preceding_tasks

    def add_preceding_task(self, task: 'Task') -> None:
        self._preceding_tasks.append(task)

    def is_necessary_for_date(self, target_date: date) -> bool:
        return self._recurrence_pattern.applies_to_date(target_date)


class Pet:
    def __init__(self, name: str, classification: PetClassification, age: int = 0, birthday: Optional[date] = None, _uuid: str = uuid4().hex):
        self._name = name
        self._classification = classification
        self._age = age
        self._birthday = birthday if birthday is not None else date.today()
        self._tasks: List[Task] = []
        self._uuid = _uuid

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

    def get_uuid(self) -> str:
        return self._uuid

    def get_tasks(self) -> List[Task]:
        return self._tasks

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)
        task.set_pet(self)

    def get_prioritized_tasks_for_date(self, target_date: date) -> List[Task]:
        pass


class ScheduleBlock(ABC):
    def __init__(self, start_time: datetime, comment: str = ""):
        self._start_time = start_time
        self._comment = comment
        self._completed = False

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

    def is_completed(self) -> bool:
        return self._completed

    def set_completed(self, completed: bool) -> None:
        self._completed = completed


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


    def __str__(self) -> str:
        start_time = self._start_time.strftime("%I:%M %p")
        hours, remainder = divmod(int(self._duration.total_seconds()), 3600)
        minutes = remainder // 60
        duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        return f"[Owner] {start_time:<12} ({duration_str})"


class TaskScheduleBlock(ScheduleBlock):
    def __init__(self, start_time: datetime, task: Task, comment: str = ""):
        super().__init__(start_time, comment)
        self._task = task

    def get_task(self) -> Task:
        return self._task

    def set_task(self, task: Task) -> None:
        self._task = task

    def get_timedelta(self) -> timedelta:
        return self._task.get_duration()


    def __str__(self) -> str:
        task_name = self._task.get_name()
        start_time = self._start_time.strftime("%I:%M %p")
        duration = self._task.get_duration()
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes = remainder // 60
        duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        pet = self._task.get_pet()
        pet_str = f" | {pet.get_name()}" if pet else ""
        status = "[✓]" if self._completed else "[ ]"
        return f"{status} {task_name:<30} {start_time:<12} ({duration_str}){pet_str}"


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

    def __str__(self) -> str:
        lines = [f"\n{'='*80}"]
        lines.append(f"Schedule for {self._date.strftime('%A, %B %d, %Y')}")
        lines.append(f"{'='*80}")
        if self._blocks:
            current_time_of_day = None
            for block in self._blocks:
                block_time_of_day = self._get_block_time_of_day(block)
                if block_time_of_day != current_time_of_day:
                    if current_time_of_day is not None:
                        lines.append(f"{'-'*80}")
                    if block_time_of_day:
                        lines.append(f"\n{block_time_of_day.name}")
                    current_time_of_day = block_time_of_day
                lines.append(str(block))
        else:
            lines.append("No blocks scheduled")
        lines.append(f"{'-'*80}")
        lines.append(f"Notes: {self._explanation}")
        lines.append(f"{'='*80}\n")
        return "\n".join(lines)

    def _get_block_time_of_day(self, block: ScheduleBlock) -> Optional[TimeOfDay]:
        if isinstance(block, TaskScheduleBlock):
            return block.get_task().get_time_of_day()
        return None


class Scheduler:
    """Singleton factory. Single scheduler instance manages all schedules.
    Access via Scheduler() or Scheduler.get_instance() — both return same instance."""
    _instance = None
    _tasks_by_time_of_day: Dict[TimeOfDay, time] = {
        TimeOfDay.MORNING: time(hour=5),
        TimeOfDay.MIDDAY: time(hour=11),
        TimeOfDay.EVENING: time(hour=17),
        TimeOfDay.NIGHT: time(hour=23)
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

        # Sort tasks within each time of day group by priority (higher first),
        # pet age (older first), then pet UUID as tiebreaker
        for time_of_day in TimeOfDay:
            tasks_by_time_of_day[time_of_day].sort(
                key=lambda x: (x[0].get_priority(), x[1].get_age(), x[1].get_uuid()),
                reverse=True
            )

        return tasks_by_time_of_day

    def _calculate_schedule_start_datetime(self, owner: Owner, target_date: date) -> datetime:
        return max(
            datetime.combine(target_date, self._tasks_by_time_of_day[TimeOfDay.MORNING]),
            datetime.combine(target_date, owner.get_available_hours_start())
        )

    def _schedule_time_period(
        self,
        schedule: Schedule,
        time_period: TimeOfDay,
        period_index: int,
        tasks: List[tuple[Task, Pet]],
        current_datetime: datetime,
        target_date: date,
        scheduled_tasks: set[tuple[Task, Pet]],
    ) -> datetime:
        period_start_datetime = datetime.combine(target_date, self._tasks_by_time_of_day[time_period])

        if current_datetime < period_start_datetime:
            current_datetime = period_start_datetime

        time_periods = list(TimeOfDay)
        if period_index < len(time_periods) - 1:
            next_period_start = datetime.combine(target_date, self._tasks_by_time_of_day[time_periods[period_index + 1]])
        else:
            next_period_start = datetime.combine(target_date, time(23, 59))

        for task, pet in tasks:
            if current_datetime >= next_period_start:
                break

            block = TaskScheduleBlock(current_datetime, task)
            schedule.add_block(block)
            scheduled_tasks.add((task, pet))
            current_datetime = current_datetime + task.get_duration()

        return current_datetime

    def _generate_schedule_explanation(
        self,
        owner: Owner,
        applicable_tasks: List[tuple[Task, Pet]],
        scheduled_tasks: set[tuple[Task, Pet]],
    ) -> str:
        missing_tasks = [(task, pet) for task, pet in applicable_tasks if (task, pet) not in scheduled_tasks]

        if missing_tasks:
            scheduled_count = len(scheduled_tasks)
            total_count = len(applicable_tasks)
            missing_details = "; ".join([f"{task.get_name()} ({pet.get_name()})" for task, pet in missing_tasks])
            return f"Scheduled {scheduled_count}/{total_count} tasks. Missing: {missing_details}."
        else:
            pet_names = [pet.get_name() for pet in owner.get_pets()]
            pets_text = ", ".join(pet_names) if pet_names else "no pets"
            return f"Pets: {pets_text}. All tasks scheduled."

    def generate_schedule(self, owner: Owner, target_date: date) -> Schedule:
        schedule = Schedule(target_date)

        tasks_by_time = self.get_task_pet_tuples_by_time_of_day_for_owner(owner, target_date)

        applicable_tasks: List[tuple[Task, Pet]] = []
        for task_list in tasks_by_time.values():
            applicable_tasks.extend(task_list)

        scheduled_tasks: set[tuple[Task, Pet]] = set()
        current_datetime = self._calculate_schedule_start_datetime(owner, target_date)

        time_periods = list(TimeOfDay)
        for i, time_period in enumerate(time_periods):
            tasks = tasks_by_time[time_period]
            current_datetime = self._schedule_time_period(
                schedule, time_period, i, tasks, current_datetime, target_date, scheduled_tasks
            )

        explanation = self._generate_schedule_explanation(owner, applicable_tasks, scheduled_tasks)
        schedule.set_explanation(explanation)

        owner.add_schedule(schedule)
        return schedule