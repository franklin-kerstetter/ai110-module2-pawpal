import streamlit as st
from datetime import timedelta
from pawpal_system import Task, DailyPattern, TimeOfDay, Pet
from components import render_sidebar_navigation

st.set_page_config(page_title="Task Configuration", layout="wide")

render_sidebar_navigation()

st.title("📋 Task Configuration")

# Check if owner and pets are configured
if not st.session_state.get("owner"):
    st.error("⚠️ Please configure your profile first in Profile Configuration")
    st.stop()

if not st.session_state.get("pets"):
    st.error("⚠️ Please add at least one pet in Profile Configuration")
    st.stop()

# Task summary across all pets
# st.markdown("### Task Summary")

with st.expander("Task Summary", expanded = True):
    summary_data = []
    for pet_name, pet in st.session_state.pets.items():
        task_count = len(pet.get_tasks())
        summary_data.append({
            "Pet": pet_name,
            "Task Count": task_count,
            "Species": pet.get_classification().name.lower()
        })

    st.table(summary_data)

st.subheader("Configure Tasks for Pets")

# Pet selection
selected_pet = st.selectbox("Select pet", list(st.session_state.pets.keys()), key="pet_select")

st.divider()

# Task input form
st.markdown("### Add New Task")

col1, col2, col3, col4 = st.columns(4)

with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title_input")

with col2:
    duration_min = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, step=5, key="task_duration_input")

with col3:
    time_of_day = st.selectbox("Time of day", [t.name.lower() for t in TimeOfDay], key="task_time_select")

with col4:
    priority = st.number_input("Priority (1-5)", min_value=1, max_value=5, value=3, step=1, key="task_priority_input")

if st.button("Add task", use_container_width=True):
    pet: Pet = st.session_state.pets[selected_pet]
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
    st.rerun()
    # st.success(f"✅ Task '{task_title}' added to {selected_pet}")

st.divider()

# Display and manage existing tasks
st.markdown("### Existing Tasks")

if st.session_state.pet_tasks.get(selected_pet):
    task_data = []
    for idx, task in enumerate(st.session_state.pet_tasks[selected_pet]):
        task_data.append({
            "Task": task.get_name(),
            "Duration (min)": int(task.get_duration().total_seconds() / 60),
            "Priority": task.get_priority(),
            "Time": task.get_time_of_day().name.lower()
        })
    st.table(task_data)

    st.markdown("### Delete Task")
    col1, col2 = st.columns([3, 1])
    with col1:
        task_to_delete = st.selectbox(
            "Select task to delete",
            [t.get_name() for t in st.session_state.pet_tasks[selected_pet]],
            key="delete_task_select"
        )
    with col2:
        if st.button("Delete", use_container_width=True):
            st.session_state.pet_tasks[selected_pet] = [
                t for t in st.session_state.pet_tasks[selected_pet]
                if t.get_name() != task_to_delete
            ]
            st.success(f"✅ Deleted '{task_to_delete}'")
            st.rerun()
else:
    st.info(f"No tasks for {selected_pet} yet. Add one above.")
