import streamlit as st


def render_sidebar_navigation():
    """Render consistent sidebar navigation across all pages."""
    st.sidebar.title("🐾 PawPal+")
    st.sidebar.divider()

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

    if st.sidebar.button("📝 Profile Configuration", use_container_width=True):
        st.switch_page("pages/1_Profile_Configuration.py")

    if st.sidebar.button("📋 Task Configuration", use_container_width=True):
        st.switch_page("pages/3_Task_Configuration.py")

    if st.sidebar.button("📅 Schedule Vault", use_container_width=True):
        st.switch_page("pages/2_Schedule_Vault.py")

    st.sidebar.divider()
