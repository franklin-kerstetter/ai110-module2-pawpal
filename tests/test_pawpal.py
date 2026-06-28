from datetime import datetime, timedelta
from pawpal_system import (
    Pet,
    Task,
    TaskScheduleBlock,
    PetClassification,
    DailyPattern,
    TimeOfDay,
)


def test_task_schedule_block_mark_complete():
    """Verify that set_completed() changes task status."""
    pet = Pet("Buddy", PetClassification.DOG, age=5)
    task = Task(
        name="Walk",
        duration=timedelta(minutes=30),
        priority=1,
        recurrence_pattern=DailyPattern(),
        time_of_day=TimeOfDay.MORNING,
        pet=pet,
    )

    block = TaskScheduleBlock(datetime(2026, 6, 28, 9, 0), task)

    assert block.is_completed() is False
    block.set_completed(True)
    assert block.is_completed() is True


def test_pet_task_count_increases_on_add():
    """Verify that adding a task to a Pet increases task count."""
    pet = Pet("Whiskers", PetClassification.CAT, age=3)

    assert len(pet.get_tasks()) == 0

    task = Task(
        name="Feed",
        duration=timedelta(minutes=5),
        priority=1,
        recurrence_pattern=DailyPattern(),
        time_of_day=TimeOfDay.MIDDAY,
    )
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0].get_name() == "Feed"
