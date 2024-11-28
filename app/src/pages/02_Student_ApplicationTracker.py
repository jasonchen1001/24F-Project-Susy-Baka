import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_application_tracker():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
        st.error("Please login as a Student to access this page.")
        st.stop()

    st.title("Application Tracking")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/00_Student_Home.py")
    
    st.divider()
    
    # Main application operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("New Application", use_container_width=True):
            st.session_state["application_action"] = "new"
            
    with col2:
        if st.button("View Applications", use_container_width=True):
            st.session_state["application_action"] = "view"
            
    with col3:
        if st.button("Application Statistics", use_container_width=True):
            st.session_state["application_action"] = "stats"

    st.divider()

    # Initialize application action if not set
    if "application_action" not in st.session_state:
        st.session_state["application_action"] = None

    # Display different sections based on selected action
    if st.session_state["application_action"] == "new":
        st.header("Submit New Application")
        with st.form("application_submit"):
            position = st.selectbox("Select Position", ["Position 1", "Position 2"])
            resume = st.selectbox("Select Resume", ["Resume v1", "Resume v2"])
            notes = st.text_area("Application Notes")
            
            if st.form_submit_button("Submit Application"):
                st.success("Application submitted successfully!")

    elif st.session_state["application_action"] == "view":
        st.header("Your Applications")
        # Add application list and status display

    elif st.session_state["application_action"] == "stats":
        st.header("Application Statistics")
        # Add statistics and analytics display

def main():
    SideBarLinks(show_home=True)
    show_application_tracker()

if __name__ == "__main__":
    main()