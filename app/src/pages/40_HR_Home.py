import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("HR Management System")
    st.write(f"Welcome, {st.session_state.get('first_name')}!")
    st.divider()

    # Create layout with columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quick Actions")
        if st.button("Manage Internship Positions", use_container_width=True):
            st.switch_page("pages/41_HR_PositionManager.py")
        if st.button("Review Applications", use_container_width=True):
            st.switch_page("pages/42_HR_ApplicationReview.py")
        if st.button("Resume Screening", use_container_width=True):
            st.switch_page("pages/43_HR_ResumeScreen.py")

    with col2:
        # Add a description or welcome message
        st.subheader("Welcome to HR Portal")
        st.write("""
        This portal provides tools to:
        - Manage internship positions
        - Review student applications
        - Screen resumes and provide feedback
        
        Select an option from the Quick Actions menu to get started.
        """)

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()