import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_resume_screen():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("Resume Screening System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    st.divider()
    
    # Main operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Review Resumes", use_container_width=True):
            st.session_state["screen_action"] = "review"
            
    with col2:
        if st.button("Screening History", use_container_width=True):
            st.session_state["screen_action"] = "history"
            
    with col3:
        if st.button("Screening Analytics", use_container_width=True):
            st.session_state["screen_action"] = "analytics"

    st.divider()

    # Initialize action if not set
    if "screen_action" not in st.session_state:
        st.session_state["screen_action"] = None

    # Display different sections based on selected action
    if st.session_state["screen_action"] == "review":
        st.header("Resume Review")
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("Student: Jane Smith")
                st.write("Resume Version: 2.0")
                st.write("Last Updated: 2023-11-15")
            with col2:
                if st.button("Provide Feedback"):
                    st.session_state["show_feedback"] = True

        if st.session_state.get("show_feedback", False):
            with st.form("feedback_form"):
                feedback = st.text_area("Enter Feedback")
                if st.form_submit_button("Submit Feedback"):
                    st.success("Feedback submitted successfully!")
                    st.session_state["show_feedback"] = False

    elif st.session_state["screen_action"] == "history":
        st.header("Screening History")
        # Add screening history display

    elif st.session_state["screen_action"] == "analytics":
        st.header("Screening Analytics")
        # Add analytics display

def main():
    SideBarLinks(show_home=True)
    show_resume_screen()

if __name__ == "__main__":
    main()
