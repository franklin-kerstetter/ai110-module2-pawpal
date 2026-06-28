import streamlit as st
from datetime import date
from pawpal_system import Scheduler
from components import render_sidebar_navigation

st.set_page_config(page_title="Schedule Vault", layout="wide")

render_sidebar_navigation()

st.title("📅 Schedule Vault")

# Initialize schedules storage if not present
if "schedules" not in st.session_state:
    st.session_state.schedules = {}

# Check if profile is set up
if not st.session_state.get("owner"):
    st.error("⚠️ Please configure your profile in the Profile Configuration page first")
    st.stop()

if not st.session_state.get("pets"):
    st.error("⚠️ Please add at least one pet in the Profile Configuration page")
    st.stop()

st.subheader("Generate Schedule")

# Date selection defaulted to today
selected_date = st.date_input("Select date", value=date.today(), key="schedule_date_select")

col1, col2 = st.columns([3, 1])

with col1:
    st.info(f"📅 Selected date: **{selected_date.strftime('%A, %B %d, %Y')}**")

with col2:
    generate_button = st.button("Generate schedule", use_container_width=True)

if generate_button:
    if not st.session_state.get("owner"):
        st.error("❌ Owner not configured")
    else:
        try:
            scheduler = Scheduler()
            schedule = scheduler.generate_schedule(st.session_state.owner, selected_date)

            # Store schedule in session state
            st.session_state.schedules[str(selected_date)] = schedule

            st.success("✅ Schedule generated!")

            # Display schedule
            st.markdown("### Generated Schedule")
            st.write(f"**Date:** {selected_date.strftime('%A, %B %d, %Y')}")
            st.write(f"**Explanation:** {schedule.get_explanation()}")

            st.markdown("#### Schedule Blocks")
            if schedule.get_blocks():
                for block in schedule.get_blocks():
                    st.write(str(block))
            else:
                st.info("No tasks scheduled for this date")

        except Exception as e:
            st.error(f"Error generating schedule: {str(e)}")

st.divider()

st.subheader("📚 Schedule History")

if st.session_state.schedules:
    # Display schedules in reverse chronological order
    sorted_dates = sorted(st.session_state.schedules.keys(), reverse=True)

    for date_str in sorted_dates:
        schedule = st.session_state.schedules[date_str]

        with st.expander(
            f"📅 {schedule.get_date().strftime('%A, %B %d, %Y')}",
            expanded=(date_str == str(selected_date))
        ):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"**Explanation:** {schedule.get_explanation()}")

                if schedule.get_blocks():
                    st.markdown("**Schedule Blocks:**")
                    for block in schedule.get_blocks():
                        st.write(str(block))
                else:
                    st.info("No tasks scheduled for this date")

            with col2:
                if st.button("Delete", key=f"delete_{date_str}"):
                    del st.session_state.schedules[date_str]
                    st.success("Schedule deleted")
                    st.rerun()

else:
    st.info("💡 No schedules generated yet. Generate one above to get started!")
