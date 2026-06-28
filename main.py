from pawpal_system import *
from datetime import date, time, timedelta

def generate_simple_testing_schedue(schedule_date: date) -> Schedule:
    owner_1 = Owner(
        name='Frank',
        available_hours_start=time(5,0),
        available_hours_end=time(20,0))
    
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
    
    feeding_tasks = generate_feeding_tasks()
    for task in feeding_tasks:
        created_pet.add_task(task)
    
    return created_pet
    

def generate_feeding_tasks() -> set:
    tasks = set()
    for i, time_of_day_enum in enumerate(list(TimeOfDay)):
        time_of_day = time_of_day_enum.name
        feeding_task = Task(name=f"{time_of_day} feeding", 
                    duration=timedelta(minutes=5),
                    priority=1,
                    recurrence_pattern=DailyPattern(),
                    time_of_day=time_of_day_enum)
        tasks.add(feeding_task)
    return tasks


# ================================================================================
#
# Start of the script execution
#
# ================================================================================

simple_schedule = generate_simple_testing_schedue(date.today())
print(f"{simple_schedule}")