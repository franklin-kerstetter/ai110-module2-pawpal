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
        """Initialize owner with name and availability window."""
        self._name = name
        self._available_hours_start = available_hours_start
        self._available_hours_end = available_hours_end
        self._pets: List['Pet'] = []
        self._schedules: Dict[date, 'Schedule'] = {}

    def get_name(self) -> str:
        """Return owner name."""
        return self._name

    def set_name(self, name: str) -> None:
        """Update owner name."""
        self._name = name

    def get_available_hours_start(self) -> time:
        """Return start of owner availability window."""
        return self._available_hours_start

    def set_available_hours_start(self, available_hours_start: time) -> None:
        """Update start of owner availability window."""
        self._available_hours_start = available_hours_start

    def get_available_hours_end(self) -> time:
        """Return end of owner availability window."""
        return self._available_hours_end

    def set_available_hours_end(self, available_hours_end: time) -> None:
        """Update end of owner availability window."""
        self._available_hours_end = available_hours_end

    def get_pets(self) -> List['Pet']:
        """Return list of owner's pets."""
        return self._pets

    def add_pet(self, pet: 'Pet') -> None:
        """Add pet to owner's collection."""
        self._pets.append(pet)

    def get_schedules(self) -> Dict[date, 'Schedule']:
        """Return dictionary of schedules keyed by date."""
        return self._schedules

    def get_schedule(self, target_date: date) -> Optional['Schedule']:
        """Return schedule for given date or None if not found."""
        return self._schedules.get(target_date)

    def add_schedule(self, schedule: 'Schedule') -> None:
        """Add schedule to owner's schedules by its date."""
        self._schedules[schedule.get_date()] = schedule


class RecurrencePattern(ABC):
    @abstractmethod
    def applies_to_date(self, target_date: date) -> bool:
        """Return True if pattern applies to the given date."""
        pass


class DailyPattern(RecurrencePattern):
    def applies_to_date(self, target_date: date) -> bool:
        """Pattern applies every day."""
        return True


class WeeklyPattern(RecurrencePattern):
    def __init__(self, days: List[int]):
        """Initialize weekly pattern with list of weekday numbers (0=Monday, 6=Sunday)."""
        if not all(0 <= day <= 6 for day in days):
            raise ValueError("Weekday numbers must be in range 0-6 (0=Monday, 6=Sunday)")
        self._days = days

    def get_days(self) -> List[int]:
        """Return list of days pattern applies to."""
        return self._days

    def set_days(self, days: List[int]) -> None:
        """Update days pattern applies to."""
        if not all(0 <= day <= 6 for day in days):
            raise ValueError("Weekday numbers must be in range 0-6 (0=Monday, 6=Sunday)")
        self._days = days

    def applies_to_date(self, target_date: date) -> bool:
        """Pattern applies if date's weekday is in the days list."""
        return target_date.weekday() in self.get_days()


class MonthlyPattern(RecurrencePattern):
    def __init__(self, day_of_month: List[int]):
        """Initialize monthly pattern with list of days (1-31)."""
        if not all(1 <= day <= 31 for day in day_of_month):
            raise ValueError("Day of month must be in range 1-31")
        self._day_of_month = day_of_month

    def get_day_of_month(self) -> List[int]:
        """Return list of days pattern applies to."""
        return self._day_of_month

    def set_day_of_month(self, day_of_month: List[int]) -> None:
        """Update days pattern applies to."""
        if not all(1 <= day <= 31 for day in day_of_month):
            raise ValueError("Day of month must be in range 1-31")
        self._day_of_month = day_of_month

    def applies_to_date(self, target_date: date) -> bool:
        """Pattern applies if date's day matches days list."""
        return target_date.day in self.get_day_of_month()


class Task:
    def __init__(self, name: str, duration: timedelta, priority: int, recurrence_pattern: RecurrencePattern, time_of_day: TimeOfDay, pet: Optional['Pet'] = None, uuid: Optional[str] = None, start_time: Optional[time] = None):
        """Initialize task with name, duration, priority, recurrence, and preferred time of day."""
        if duration <= timedelta(0):
            raise ValueError("Task duration must be greater than zero")
        self._name = name
        self._duration = duration
        self._priority = priority
        self._recurrence_pattern = recurrence_pattern
        self._time_of_day = time_of_day
        self._pet = pet
        self._start_time = start_time
        self._preceding_tasks: List[Task] = []
        self._uuid = uuid if uuid is not None else uuid4().hex

    def get_name(self) -> str:
        """Return task name."""
        return self._name

    def set_name(self, name: str) -> None:
        """Update task name."""
        self._name = name

    def get_duration(self) -> timedelta:
        """Return task duration."""
        return self._duration

    def set_duration(self, duration: timedelta) -> None:
        """Update task duration."""
        self._duration = duration

    def get_priority(self) -> int:
        """Return task priority."""
        return self._priority

    def set_priority(self, priority: int) -> None:
        """Update task priority."""
        self._priority = priority

    def get_recurrence_pattern(self) -> RecurrencePattern:
        """Return task recurrence pattern."""
        return self._recurrence_pattern

    def set_recurrence_pattern(self, recurrence_pattern: RecurrencePattern) -> None:
        """Update task recurrence pattern."""
        self._recurrence_pattern = recurrence_pattern

    def get_time_of_day(self) -> TimeOfDay:
        """Return preferred time of day for task."""
        return self._time_of_day

    def set_time_of_day(self, time_of_day: TimeOfDay) -> None:
        """Update preferred time of day for task."""
        self._time_of_day = time_of_day

    def get_start_time(self) -> Optional[time]:
        """Return specified start time for task."""
        return self._start_time

    def set_start_time(self, start_time: Optional[time]) -> None:
        """Update specified start time for task."""
        self._start_time = start_time

    def get_pet(self) -> Optional['Pet']:
        """Return pet this task belongs to."""
        return self._pet

    def set_pet(self, pet: Optional['Pet']) -> None:
        """Update pet this task belongs to."""
        self._pet = pet

    def get_preceding_tasks(self) -> List['Task']:
        """Return list of tasks that must complete before this task."""
        return self._preceding_tasks

    def add_preceding_task(self, task: 'Task') -> None:
        """Add task that must complete before this task."""
        self._preceding_tasks.append(task)

    def is_necessary_for_date(self, target_date: date) -> bool:
        """Return True if task applies to the given date based on recurrence pattern."""
        return self.get_recurrence_pattern().applies_to_date(target_date)


class Pet:
    def __init__(self, name: str, classification: PetClassification, age: int = 0, birthday: Optional[date] = None, _uuid: Optional[str] = None):
        """Initialize pet with name, classification, age, and birthday."""
        self._name = name
        self._classification = classification
        self._age = age
        self._birthday = birthday if birthday is not None else date.today()
        self._tasks: List[Task] = []
        self._uuid = _uuid if _uuid is not None else uuid4().hex

    def get_name(self) -> str:
        """Return pet name."""
        return self._name

    def set_name(self, name: str) -> None:
        """Update pet name."""
        self._name = name

    def get_classification(self) -> PetClassification:
        """Return pet type classification."""
        return self._classification

    def set_classification(self, classification: PetClassification) -> None:
        """Update pet type classification."""
        self._classification = classification

    def get_age(self) -> int:
        """Return pet age in years."""
        return self._age

    def set_age(self, age: int) -> None:
        """Update pet age."""
        self._age = age

    def get_birthday(self) -> date:
        """Return pet birthday."""
        return self._birthday

    def set_birthday(self, birthday: date) -> None:
        """Update pet birthday."""
        self._birthday = birthday

    def get_uuid(self) -> str:
        """Return unique identifier for pet."""
        return self._uuid

    def get_tasks(self) -> List[Task]:
        """Return list of tasks for pet."""
        return self._tasks

    def add_task(self, task: Task) -> None:
        """Add task to pet and set task's pet reference."""
        self._tasks.append(task)
        task.set_pet(self)


class ScheduleBlock(ABC):
    def __init__(self, start_time: datetime, comment: str = ""):
        """Initialize schedule block with start time and optional comment."""
        self._start_time = start_time
        self._comment = comment
        self._completed = False

    def get_start_time(self) -> datetime:
        """Return start time of block."""
        return self._start_time

    def set_start_time(self, start_time: datetime) -> None:
        """Update start time of block."""
        self._start_time = start_time

    def get_comment(self) -> str:
        """Return comment for block."""
        return self._comment

    def set_comment(self, comment: str) -> None:
        """Update comment for block."""
        self._comment = comment

    def is_completed(self) -> bool:
        """Return True if block is marked completed."""
        return self._completed

    def set_completed(self, completed: bool) -> None:
        """Set completion status of block."""
        self._completed = completed

    def mark_completed(self) -> None:
        """Mark block as completed."""
        self.set_completed(True)

    def unmark_completed(self) -> None:
        """Mark block as not completed."""
        self.set_completed(False)

    @abstractmethod
    def get_timedelta(self) -> timedelta:
        """Return duration of block."""
        pass

    @staticmethod
    def get_block_time_of_day(block: 'ScheduleBlock') -> Optional[TimeOfDay]:
        """Return time of day for block if it's a TaskScheduleBlock."""
        if isinstance(block, TaskScheduleBlock):
            return block.get_time_of_day()
        return None


class OwnerScheduleBlock(ScheduleBlock):
    def __init__(self, start_time: datetime, duration: timedelta, comment: str = ""):
        """Initialize owner availability block with start time and duration."""
        super().__init__(start_time, comment)
        self._duration = duration

    def get_duration(self) -> timedelta:
        """Return duration of owner availability."""
        return self._duration

    def set_duration(self, duration: timedelta) -> None:
        """Update duration of owner availability."""
        self._duration = duration

    def get_timedelta(self) -> timedelta:
        """Return duration of block."""
        return self._duration

    def __str__(self) -> str:
        """Return formatted string representation of owner block."""
        start_time = self.get_start_time().strftime("%I:%M %p")
        hours, remainder = divmod(int(self.get_duration().total_seconds()), 3600)
        minutes = remainder // 60
        duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        return f"[Owner] {start_time:<12} ({duration_str})"


class TaskScheduleBlock(ScheduleBlock):
    def __init__(self, start_time: datetime, task: Task, comment: str = ""):
        """Initialize task schedule block with start time and task."""
        super().__init__(start_time, comment)
        self._task = task

    def get_task(self) -> Task:
        """Return the task assigned to this block."""
        return self._task

    def set_task(self, task: Task) -> None:
        """Update the task assigned to this block."""
        self._task = task

    def get_timedelta(self) -> timedelta:
        """Return duration of task."""
        return self._task.get_duration()

    def get_time_of_day(self) -> TimeOfDay:
        """Return preferred time of day for task."""
        return self._task.get_time_of_day()

    def __str__(self) -> str:
        """Return formatted string representation of task block."""
        task_name = self.get_task().get_name()
        start_time = self.get_start_time().strftime("%I:%M %p")
        duration = self.get_task().get_duration()
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes = remainder // 60
        duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        pet = self.get_task().get_pet()
        pet_str = f" | {pet.get_name()}" if pet else ""
        status = "[✓]" if self.is_completed() else "[ ]"
        return f"{status} {task_name:<30} {start_time:<12} ({duration_str}){pet_str}"


class Schedule:
    def __init__(self, date: date, explanation: str = ""):
        """Initialize schedule for a specific date."""
        self._date = date
        self._explanation = explanation
        self._blocks: List[ScheduleBlock] = []

    def get_date(self) -> date:
        """Return date of schedule."""
        return self._date

    def set_date(self, date: date) -> None:
        """Update date of schedule."""
        self._date = date

    def get_explanation(self) -> str:
        """Return explanation notes for schedule."""
        return self._explanation

    def set_explanation(self, explanation: str) -> None:
        """Update explanation notes for schedule."""
        self._explanation = explanation

    def get_blocks(self) -> List[ScheduleBlock]:
        """Return list of schedule blocks."""
        return self._blocks

    def add_block(self, block: ScheduleBlock) -> None:
        """Add schedule block to schedule."""
        self._blocks.append(block)

    def __str__(self) -> str:
        """Return formatted string representation of schedule grouped by time of day."""
        lines = [f"\n{'='*80}"]
        lines.append(f"Schedule for {self.get_date().strftime('%A, %B %d, %Y')}")
        lines.append(f"{'='*80}")
        if self.get_blocks():
            current_time_of_day = None
            for block in self.get_blocks():
                block_time_of_day = ScheduleBlock.get_block_time_of_day(block)
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
        lines.append(f"Notes: {self.get_explanation()}")
        lines.append(f"{'='*80}\n")
        return "\n".join(lines)


class Scheduler:
    """Singleton factory. Single scheduler instance manages all schedules.
    Access via Scheduler() or Scheduler.get_instance() — both return same instance."""
    _instance = None
    _TIME_OF_DAY_TIMES: Dict[TimeOfDay, time] = {
        TimeOfDay.MORNING: time(hour=5),
        TimeOfDay.MIDDAY: time(hour=11),
        TimeOfDay.EVENING: time(hour=17),
        TimeOfDay.NIGHT: time(hour=23)
    }
    _TIME_PERIODS = list(TimeOfDay)

    def __new__(cls):
        """Enforce singleton pattern for scheduler."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'Scheduler':
        """Return singleton scheduler instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def _get_sort_key_for_task_pet_tuple(task_pet_tuple: tuple[Task, Pet]) -> tuple:
        """Return sort key tuple for a task-pet pair."""
        task, pet = task_pet_tuple
        return (task.get_time_of_day().value, -task.get_priority(), -pet.get_age(), pet.get_uuid())

    def sort_task_pet_tuples_by_time(self, task_pet_tuples: List[tuple[Task, Pet]]) -> List[tuple[Task, Pet]]:
        """Return task-pet tuples sorted by time of day, priority, age, and UUID."""
        return sorted(task_pet_tuples, key=self._get_sort_key_for_task_pet_tuple)

    def sort_by_time(self, tasks: List[Task]) -> List[tuple[Task, Pet]]:
        """Return tasks with their pets sorted by time of day, priority, age, and UUID."""
        task_pet_tuples = [(task, task.get_pet()) for task in tasks]
        return self.sort_task_pet_tuples_by_time(task_pet_tuples)

    def filter_tasks_by_pet_name(self, task_pet_tuples: List[tuple[Task, Pet]], pet_name: str) -> List[tuple[Task, Pet]]:
        """Return task-pet tuples filtered by pet name."""
        return [task_pet for task_pet in task_pet_tuples if task_pet[1].get_name() == pet_name]

    def filter_blocks_by_completion_status(self, blocks: List[ScheduleBlock], completed: bool) -> List[ScheduleBlock]:
        """Return schedule blocks filtered by completion status."""
        return [block for block in blocks if block.is_completed() == completed]

    def detect_schedule_conflicts(self, schedule: Schedule) -> List[str]:
        """Detect task scheduling conflicts and return list of warning messages."""
        warnings = []
        blocks = schedule.get_blocks()
        task_blocks = [block for block in blocks if isinstance(block, TaskScheduleBlock)]

        for i, block1 in enumerate(task_blocks):
            for block2 in task_blocks[i + 1:]:
                end_time1 = block1.get_start_time() + block1.get_timedelta()
                end_time2 = block2.get_start_time() + block2.get_timedelta()

                if block1.get_start_time() < end_time2 and block2.get_start_time() < end_time1:
                    task1 = block1.get_task()
                    task2 = block2.get_task()
                    pet1 = task1.get_pet()
                    pet2 = task2.get_pet()

                    pet1_name = pet1.get_name() if pet1 else "Unknown"
                    pet2_name = pet2.get_name() if pet2 else "Unknown"

                    conflict_type = "same pet" if pet1 == pet2 else "different pets"
                    warning = f"Conflict: '{task1.get_name()}' ({pet1_name}) and '{task2.get_name()}' ({pet2_name}) overlap [{conflict_type}]"
                    warnings.append(warning)

        return warnings

    def get_task_pet_tuples_by_time_of_day_for_owner(self, owner: Owner, target_date: date) -> Dict[TimeOfDay, List[tuple[Task, Pet]]]:
        """Return owner's tasks grouped by time of day and sorted by priority for target date."""
        # Collect all applicable tasks from each pet
        all_tasks: List[tuple[Task, Pet]] = []
        for pet in owner.get_pets():
            for task in pet.get_tasks():
                if task.is_necessary_for_date(target_date):
                    all_tasks.append((task, pet))

        # Sort once by time of day, priority (higher first), pet age (older first), then UUID
        all_tasks = self.sort_task_pet_tuples_by_time(all_tasks)

        # Group by time of day (already sorted within each group)
        tasks_by_time_of_day: Dict[TimeOfDay, List[tuple[Task, Pet]]] = {
            time_of_day: [] for time_of_day in TimeOfDay
        }
        for task, pet in all_tasks:
            tasks_by_time_of_day[task.get_time_of_day()].append((task, pet))

        return tasks_by_time_of_day

    def _calculate_schedule_start_datetime(self, owner: Owner, target_date: date) -> datetime:
        """Calculate schedule start time as max of morning time and owner availability start."""
        return max(
            datetime.combine(target_date, self._TIME_OF_DAY_TIMES[TimeOfDay.MORNING]),
            datetime.combine(target_date, owner.get_available_hours_start())
        )

    def _retry_unfit_tasks(
        self,
        schedule: Schedule,
        unfit_tasks: List[tuple[Task, Pet]],
        current_datetime: datetime,
        next_period_start: datetime,
        scheduled_tasks: set[tuple[Task, Pet]],
        owner_end_datetime: datetime,
    ) -> datetime:
        """Retry tasks that couldn't be scheduled, returning updated current time."""
        while unfit_tasks:
            scheduled_in_pass = False
            remaining_unfit = []
            for task, pet in unfit_tasks:
                if current_datetime >= next_period_start:
                    remaining_unfit.append((task, pet))
                    continue

                preceding_scheduled = all(
                    (pt, pt.get_pet()) in scheduled_tasks
                    for pt in task.get_preceding_tasks()
                )
                if not preceding_scheduled:
                    remaining_unfit.append((task, pet))
                    continue

                task_end_datetime = current_datetime + task.get_duration()
                if task_end_datetime > owner_end_datetime:
                    remaining_unfit.append((task, pet))
                    continue

                block = TaskScheduleBlock(current_datetime, task)
                schedule.add_block(block)
                scheduled_tasks.add((task, pet))
                current_datetime = task_end_datetime
                scheduled_in_pass = True

            unfit_tasks = remaining_unfit
            if not scheduled_in_pass:
                break

        return current_datetime

    def _schedule_time_period(
        self,
        schedule: Schedule,
        time_period: TimeOfDay,
        period_index: int,
        tasks: List[tuple[Task, Pet]],
        current_datetime: datetime,
        target_date: date,
        scheduled_tasks: set[tuple[Task, Pet]],
        owner_end_datetime: datetime,
    ) -> datetime:
        """Schedule tasks for a specific time period, returning updated current time."""
        period_start_datetime = datetime.combine(target_date, self._TIME_OF_DAY_TIMES[time_period])

        if current_datetime < period_start_datetime:
            current_datetime = period_start_datetime

        if period_index < len(self._TIME_PERIODS) - 1:
            next_period_start = datetime.combine(target_date, self._TIME_OF_DAY_TIMES[self._TIME_PERIODS[period_index + 1]])
        else:
            next_period_start = datetime.combine(target_date, time(23, 59))

        unfit_tasks = []
        for task, pet in tasks:
            if current_datetime >= next_period_start:
                break

            preceding_scheduled = all(
                (pt, pt.get_pet()) in scheduled_tasks
                for pt in task.get_preceding_tasks()
            )
            if not preceding_scheduled:
                unfit_tasks.append((task, pet))
                continue

            task_end_datetime = current_datetime + task.get_duration()
            if task_end_datetime > owner_end_datetime:
                unfit_tasks.append((task, pet))
                continue

            block = TaskScheduleBlock(current_datetime, task)
            schedule.add_block(block)
            scheduled_tasks.add((task, pet))
            current_datetime = task_end_datetime

        if unfit_tasks:
            current_datetime = self._retry_unfit_tasks(
                schedule, unfit_tasks, current_datetime, next_period_start, scheduled_tasks, owner_end_datetime
            )

        return current_datetime

    def _generate_schedule_explanation(
        self,
        applicable_tasks: set[tuple[Task, Pet]],
        scheduled_tasks: set[tuple[Task, Pet]],
    ) -> str:
        """Generate explanation text describing scheduled and missing tasks."""
        missing_tasks = applicable_tasks - scheduled_tasks

        if missing_tasks:
            scheduled_count = len(scheduled_tasks)
            total_count = len(applicable_tasks)

            missing_by_time = {}
            for task, pet in missing_tasks:
                time_of_day = task.get_time_of_day().name
                if time_of_day not in missing_by_time:
                    missing_by_time[time_of_day] = []
                missing_by_time[time_of_day].append(f"{task.get_name()} ({pet.get_name()})")

            missing_details = "; ".join(
                f"{time_of_day}: {', '.join(tasks)}"
                for time_of_day, tasks in missing_by_time.items()
            )
            return f"Scheduled {scheduled_count}/{total_count} tasks. Missing: {missing_details}."
        else:
            return "All tasks scheduled."

    def generate_schedule(self, owner: Owner, target_date: date) -> Schedule:
        """Generate complete schedule for owner on target date."""
        schedule = Schedule(target_date)

        tasks_by_time = self.get_task_pet_tuples_by_time_of_day_for_owner(owner, target_date)

        applicable_tasks: set[tuple[Task, Pet]] = set()
        for task_list in tasks_by_time.values():
            applicable_tasks.update(task_list)

        scheduled_tasks: set[tuple[Task, Pet]] = set()
        current_datetime = self._calculate_schedule_start_datetime(owner, target_date)
        owner_end_datetime = datetime.combine(target_date, owner.get_available_hours_end())

        for i, time_period in enumerate(self._TIME_PERIODS):
            tasks = tasks_by_time[time_period]
            current_datetime = self._schedule_time_period(
                schedule, time_period, i, tasks, current_datetime, target_date, scheduled_tasks, owner_end_datetime
            )

        explanation = self._generate_schedule_explanation(applicable_tasks, scheduled_tasks)
        schedule.set_explanation(explanation)

        owner.add_schedule(schedule)
        return schedule