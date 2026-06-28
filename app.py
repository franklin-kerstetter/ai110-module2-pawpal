import streamlit as st
from datetime import date
from pawpal_system import Scheduler
from components import render_sidebar_navigation

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

render_sidebar_navigation()

st.title("🐾 PawPal+")

# Check if owner is configured
if not st.session_state.get("owner"):
    st.info("👋 Welcome to PawPal+! Start by going to **Profile Configuration** to set up your account.")

    with st.expander("What is PawPal+?", expanded=True):
        st.markdown(
            """
            **PawPal+** is your personal pet care planning assistant that helps you:
            - Manage care tasks for your pet(s)
            - Schedule tasks based on your availability
            - Never forget important pet care routines
            - View and organize your pet care schedule
            """
        )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            ### 📝 Step 1: Profile Configuration
            - Set your availability window
            - Add your pets
            - Create care tasks for each pet
            """
        )

    with col2:
        st.markdown(
            """
            ### 📅 Step 2: Schedule Vault
            - Generate daily schedules
            - View your schedule history
            - Get AI-powered scheduling
            """
        )
else:
    # Show owner dashboard
    owner = st.session_state.owner

    # Owner info section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👤 Owner", owner.get_name())

    with col2:
        start_hour = owner.get_available_hours_start().hour
        end_hour = owner.get_available_hours_end().hour
        st.metric("⏰ Available", f"{start_hour}:00 - {end_hour}:00")

    with col3:
        pet_count = len(st.session_state.get("pets", {}))
        st.metric("🐾 Pets", pet_count)

    st.divider()

    # Pets section
    st.subheader("Your Pets")

    if st.session_state.get("pets"):
        cols = st.columns(len(st.session_state.pets))
        for idx, (pet_name, pet) in enumerate(st.session_state.pets.items()):
            with cols[idx]:
                task_count = len(pet.get_tasks())
                st.write(f"**{pet_name}**")
                st.caption(f"{pet.get_classification().name.lower()} • {task_count} tasks")
    else:
        st.info("No pets configured yet. Go to Profile Configuration to add one.")

    st.divider()

    # Today's schedule section
    st.subheader("📅 Today's Schedule")

    today = date.today()
    today_str = str(today)
    schedules = st.session_state.get("schedules", {})

    if today_str in schedules:
        # Display existing schedule
        schedule = schedules[today_str]

        st.success(f"✅ Schedule for {today.strftime('%A, %B %d, %Y')}")
        st.write(f"**{schedule.get_explanation()}**")

        if schedule.get_blocks():
            st.markdown("### Schedule Blocks:")
            for block in schedule.get_blocks():
                st.write(str(block))
        else:
            st.info("No tasks scheduled for today")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Regenerate today's schedule"):
                try:
                    scheduler = Scheduler()
                    new_schedule = scheduler.generate_schedule(owner, today)
                    st.session_state.schedules[today_str] = new_schedule
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating schedule: {str(e)}")

        with col2:
            if st.button("📅 Go to Schedule Vault"):
                st.switch_page("pages/2_Schedule_Vault.py")
    else:
        # No schedule for today
        st.info("No schedule generated for today yet.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📅 Generate today's schedule", use_container_width=True):
                try:
                    scheduler = Scheduler()
                    schedule = scheduler.generate_schedule(owner, today)
                    st.session_state.schedules[today_str] = schedule
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating schedule: {str(e)}")

        with col2:
            if st.button("📅 Go to Schedule Vault", use_container_width=True):
                st.switch_page("pages/2_Schedule_Vault.py")
