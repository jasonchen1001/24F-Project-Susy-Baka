import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests
from datetime import datetime

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_resume_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
        st.error("Please login as a Student to access this page.")
        st.stop()

    st.title("Resume Management")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/00_Student_Home.py")
    
    st.divider()
    
    # Main resume operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Upload New Resume", use_container_width=True):
            st.session_state["resume_action"] = "upload"
            
    with col2:
        if st.button("View Resumes", use_container_width=True):
            st.session_state["resume_action"] = "view"
            
    with col3:
        if st.button("Resume Feedback", use_container_width=True):
            st.session_state["resume_action"] = "feedback"

    st.divider()

    # Initialize resume action if not set
    if "resume_action" not in st.session_state:
        st.session_state["resume_action"] = None

    # Display different sections based on selected action
    if st.session_state["resume_action"] == "upload":
        st.header("Upload New Resume")
        with st.form("resume_upload"):
            uploaded_file = st.file_uploader("Choose resume file", type=['pdf', 'docx'])
            version_notes = st.text_area("Version Notes")
            
            if st.form_submit_button("Upload"):
                if uploaded_file is not None:
                    # Add your file upload logic here
                    st.success("Resume uploaded successfully!")
                else:
                    st.error("Please select a file to upload")

    elif st.session_state["resume_action"] == "view":
        st.header("Your Resumes")
        # Add resume list and preview functionality

    elif st.session_state["resume_action"] == "feedback":
        st.header("Resume Feedback")
        # Add feedback display and interaction

def main():
    SideBarLinks(show_home=True)
    show_resume_manager()

if __name__ == "__main__":
    main()