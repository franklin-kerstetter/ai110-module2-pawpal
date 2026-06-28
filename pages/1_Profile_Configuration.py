import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, PetClassification
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
            new_pet = Pet(pet_name, pet_classification)
            st.session_state.pets[pet_name] = new_pet
            st.session_state.owner.add_pet(new_pet)
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
            st.metric(pet.get_classification().name.lower(), pet_name)
else:
    st.info("No pets yet. Add one above.")

st.divider()

# Link to task configuration
st.info("💡 Go to **Task Configuration** page to add and manage tasks for your pets.")
