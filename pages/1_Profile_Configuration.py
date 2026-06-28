import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, PetClassification, Task, DailyPattern, TimeOfDay
from datetime import timedelta
from components import render_sidebar_navigation

st.set_page_config(page_title="Profile Configuration", layout="wide")

render_sidebar_navigation()

st.title("⚙️ Profile Configuration")

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None

if "pets" not in st.session_state:
    st.session_state.pets = {}  # pet_name -> Pet object

if "pet_tasks" not in st.session_state:
    st.session_state.pet_tasks = {}  # pet_name -> list of Task objects

# Owner Setup
st.subheader("Owner Info")
col1, col2, col3 = st.columns(3)

with col1:
    owner_name = st.text_input("Owner name", value="Jordan", key="owner_name_input")

with col2:
    start_hour = st.number_input("Available from (hour)", min_value=0, max_value=23, value=8, step=1)

with col3:
    end_hour = st.number_input("Available until (hour)", min_value=0, max_value=23, value=20, step=1)

if st.button("Save owner"):
    if start_hour >= end_hour:
        st.error("Start time must be before end time")
    else:
        st.session_state.owner = Owner(
            owner_name,
            time(start_hour, 0),
            time(end_hour, 0)
        )
        st.success(f"Owner '{owner_name}' saved (Available {start_hour}:00 - {end_hour}:00)")

if st.session_state.owner:
    st.info(
        f"✅ Current owner: {st.session_state.owner.get_name()} "
        f"(Available {st.session_state.owner.get_available_hours_start().hour}:00 - "
        f"{st.session_state.owner.get_available_hours_end().hour}:00)"
    )
else:
    st.warning("⚠️ Please configure owner info above")

st.divider()

# Pet Management
st.subheader("Pets")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    pet_name = st.text_input("Pet name", key="pet_name_input")

with col2:
    species = st.selectbox("Species", [cls.name.lower() for cls in list(PetClassification)], key="species_select")

with col3:
    if st.button("Add pet"):
        if pet_name and pet_name not in st.session_state.pets:
            pet_classification = PetClassification[species.upper()]
            st.session_state.pets[pet_name] = Pet(pet_name, pet_classification)
            st.session_state.pet_tasks[pet_name] = []
            st.success(f"✅ Added {pet_name} ({species})")
        elif pet_name in st.session_state.pets:
            st.error(f"Pet '{pet_name}' already exists")
        else:
            st.error("Enter pet name")

if st.session_state.pets:
    st.write("**Your Pets:**")
    cols = st.columns(len(st.session_state.pets))
    for idx, (pet_name, pet) in enumerate(st.session_state.pets.items()):
        with cols[idx]:
            st.metric(pet_name, pet.get_classification().name.lower())
else:
    st.info("No pets yet. Add one above.")

st.divider()

# Task Management per Pet
if st.session_state.pets:
    st.subheader("Configure Tasks")
    selected_pet = st.selectbox("Select pet", list(st.session_state.pets.keys()), key="pet_select")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title_input")

    with col2:
        duration_min = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, step=5, key="task_duration_input")

    with col3:
        time_of_day = st.selectbox("Time of day", [t.name.lower() for t in TimeOfDay], key="task_time_select")

    with col4:
        priority = st.number_input("Priority (1-5)", min_value=1, max_value=5, value=3, step=1, key="task_priority_input")

    if st.button("Add task to pet"):
        pet = st.session_state.pets[selected_pet]
        task = Task(
            name=task_title,
            duration=timedelta(minutes=duration_min),
            priority=priority,
            recurrence_pattern=DailyPattern(),
            time_of_day=TimeOfDay[time_of_day.upper()],
            pet=pet
        )
        pet.add_task(task)
        st.session_state.pet_tasks[selected_pet].append(task)
        st.success(f"✅ Task '{task_title}' added to {selected_pet}")

    # Display tasks for selected pet
    if st.session_state.pet_tasks[selected_pet]:
        st.write(f"**Tasks for {selected_pet}:**")
        task_data = []
        for idx, task in enumerate(st.session_state.pet_tasks[selected_pet]):
            task_data.append({
                "Task": task.get_name(),
                "Duration (min)": int(task.get_duration().total_seconds() / 60),
                "Priority": task.get_priority(),
                "Time": task.get_time_of_day().name.lower()
            })
        st.table(task_data)

        # Delete task option
        if st.session_state.pet_tasks[selected_pet]:
            col1, col2 = st.columns([3, 1])
            with col1:
                task_to_delete = st.selectbox(
                    "Delete task",
                    [t.get_name() for t in st.session_state.pet_tasks[selected_pet]],
                    key="delete_task_select"
                )
            with col2:
                if st.button("Delete"):
                    st.session_state.pet_tasks[selected_pet] = [
                        t for t in st.session_state.pet_tasks[selected_pet]
                        if t.get_name() != task_to_delete
                    ]
                    st.success(f"✅ Deleted '{task_to_delete}'")
    else:
        st.info(f"No tasks for {selected_pet} yet. Add one above.")
else:
    st.info("⚠️ Add a pet first to configure tasks")
