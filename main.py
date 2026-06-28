from pawpal_system import *
from datetime import date, time, timedelta

def generate_simple_testing_schedue(schedule_date: date) -> Schedule:
    owner_1 = Owner(
        name='Frank',
        available_hours_start=time(5,0),
        available_hours_end=time(23,59))
    
    # Create 1st pet - ARCHIE - DOG
    pet_1 = create_pet_with_feeding_tasks(
        name="Archie",
        classification=PetClassification.DOG,
        age=1,
        birthday=date(2025, 10, 11)
        )
    owner_1.add_pet(pet_1)
        
    # Create 2nd pet - QUEEN - FISH
    pet_2 = create_pet_with_feeding_tasks(
        name="Queen",
        classification=PetClassification.FISH,
        age=2,
        birthday=date(2024, 6, 17)
        )
    owner_1.add_pet(pet_2)

    scheduler = Scheduler()
    owner_1_schedule = scheduler.generate_schedule(owner_1, schedule_date)

    return owner_1_schedule    
    

def create_pet_with_feeding_tasks(name: str, classification: PetClassification, age: int, birthday: date) -> Pet:
    created_pet = Pet(name, classification, age, birthday)
    
    feeding_tasks = generate_feeding_tasks(name)
    for task in feeding_tasks:
        created_pet.add_task(task)
    
    return created_pet
    

def generate_feeding_tasks(pet_name: str="My Pet") -> set:
    tasks = set()
    for i, time_of_day_enum in enumerate(list(TimeOfDay)):
        time_of_day = time_of_day_enum.name
        feeding_task = Task(name=f"Feed {pet_name}", 
                    duration=timedelta(minutes=5),
                    priority=1,
                    recurrence_pattern=DailyPattern(),
                    time_of_day=time_of_day_enum)
        tasks.add(feeding_task)
    return tasks

def mark_morning_tasks_as_completed(schedule: Schedule) -> None:
    for schedule_block in schedule.get_blocks():
        if ScheduleBlock.get_block_time_of_day(schedule_block) == TimeOfDay.MORNING:
            schedule_block.mark_completed()


def generate_tasks_with_explicit_times(pet_name: str="My Pet") -> set:
    tasks = set()
    explicit_times = [
        (TimeOfDay.EVENING, time(17, 30)),
        (TimeOfDay.MORNING, time(6, 0)),
        (TimeOfDay.NIGHT, time(22, 0)),
        (TimeOfDay.MIDDAY, time(12, 30)),
    ]
    for time_of_day, explicit_time in explicit_times:
        feeding_task = Task(
            name=f"Feed {pet_name}",
            duration=timedelta(minutes=5),
            priority=1,
            recurrence_pattern=DailyPattern(),
            time_of_day=time_of_day,
            start_time=explicit_time
        )
        tasks.add(feeding_task)
    return tasks


def create_pet_with_explicit_time_tasks(name: str, classification: PetClassification, age: int, birthday: date) -> Pet:
    created_pet = Pet(name, classification, age, birthday)
    tasks = generate_tasks_with_explicit_times(name)
    for task in tasks:
        created_pet.add_task(task)
    return created_pet


def generate_complex_testing_schedule(schedule_date: date) -> Schedule:
    owner_2 = Owner(
        name='Alex',
        available_hours_start=time(6, 0),
        available_hours_end=time(22, 0)
    )

    # Create pets with tasks having explicit start times (out of order)
    pet_3 = create_pet_with_explicit_time_tasks(
        name="Fluffy",
        classification=PetClassification.CAT,
        age=3,
        birthday=date(2023, 3, 15)
    )
    owner_2.add_pet(pet_3)

    pet_4 = create_pet_with_explicit_time_tasks(
        name="Buddy",
        classification=PetClassification.DOG,
        age=5,
        birthday=date(2021, 1, 20)
    )
    owner_2.add_pet(pet_4)

    scheduler = Scheduler()
    owner_2_schedule = scheduler.generate_schedule(owner_2, schedule_date)

    return owner_2_schedule


# ================================================================================
#
# Start of the script execution
#
# ================================================================================


# ================================================================================
#
# Simple Schedule Creation
#
# ================================================================================

print(f"Test generating simple schedule")
simple_schedule = generate_simple_testing_schedue(date.today())
print(f"{simple_schedule}")

mark_morning_tasks_as_completed(simple_schedule)
print(f"Test marking morning tasks as done!")
print(f"{simple_schedule}")


# ================================================================================
#
# Complex Schedule with Explicit Times and Sorting/Filtering Demo
#
# ================================================================================

print(f"Test generating complex schedule")
complex_schedule = generate_complex_testing_schedule(date.today())
print(f"{complex_schedule}")

# Mark some tasks as completed for filtering demo
for i, schedule_block in enumerate(complex_schedule.get_blocks()):
    if i % 2 == 0:
        schedule_block.mark_completed()

print("\n" + "="*80)
print("SORTING AND FILTERING DEMONSTRATION")
print("="*80 + "\n")

# Get all blocks from the schedule
all_blocks = complex_schedule.get_blocks()

# Filter: Show only completed blocks
completed_blocks = Scheduler().filter_blocks_by_completion_status(all_blocks, completed=True)
print(f"Completed Blocks ({len(completed_blocks)}):")
for block in completed_blocks:
    print(f"  {block}")

print()

# Filter: Show only uncompleted blocks
uncompleted_blocks = Scheduler().filter_blocks_by_completion_status(all_blocks, completed=False)
print(f"Uncompleted Blocks ({len(uncompleted_blocks)}):")
for block in uncompleted_blocks:
    print(f"  {block}")

print("\n" + "-"*80 + "\n")

# Sorting: Get all tasks from the schedule, extract them, and sort by time
scheduler = Scheduler()
all_task_pet_tuples = []
for block in all_blocks:
    if isinstance(block, TaskScheduleBlock):
        task = block.get_task()
        pet = task.get_pet()
        if pet and (task, pet) not in all_task_pet_tuples:
            all_task_pet_tuples.append((task, pet))

all_tasks = [task for task, pet in all_task_pet_tuples]
sorted_tasks = scheduler.sort_by_time(all_tasks)

print(f"All Tasks Sorted by Time of Day, Priority, and Pet Age:")
for task, pet in sorted_tasks:
    pet_name = pet.get_name() if pet else "Unknown"
    time_of_day = task.get_time_of_day().name
    explicit_time = f" (explicit: {task.get_start_time()})" if task.get_start_time() else ""
    print(f"  {task.get_name()} | {pet_name} | {time_of_day}{explicit_time}")

print("\n" + "-"*80 + "\n")

# Filter: Show tasks for specific pet
fluffy_tasks = scheduler.filter_tasks_by_pet_name(sorted_tasks, "Fluffy")
print(f"Tasks for Fluffy ({len(fluffy_tasks)}):")
for task, pet in fluffy_tasks:
    time_of_day = task.get_time_of_day().name
    explicit_time = f" (explicit: {task.get_start_time()})" if task.get_start_time() else ""
    print(f"  {task.get_name()} | {time_of_day}{explicit_time}")

print("\n" + "-"*80 + "\n")

# Filter: Show tasks for different pet
buddy_tasks = scheduler.filter_tasks_by_pet_name(sorted_tasks, "Buddy")
print(f"Tasks for Buddy ({len(buddy_tasks)}):")
for task, pet in buddy_tasks:
    time_of_day = task.get_time_of_day().name
    explicit_time = f" (explicit: {task.get_start_time()})" if task.get_start_time() else ""
    print(f"  {task.get_name()} | {time_of_day}{explicit_time}")