import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_grade_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "School_Admin":
        st.error("Please login as School Administrator to access this page.")
        st.stop()

    st.title("Grade Management System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/20_Admin_Home.py")
    
    st.divider()
    
    # Main operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Record Grades", use_container_width=True):
            st.session_state["grade_action"] = "record"
            
    with col2:
        if st.button("View Grade Records", use_container_width=True):
            st.session_state["grade_action"] = "view"
            
    with col3:
        if st.button("Grade Analytics", use_container_width=True):
            st.session_state["grade_action"] = "analytics"

    st.divider()

    # Initialize action if not set
    if "grade_action" not in st.session_state:
        st.session_state["grade_action"] = None

    # Display different sections based on selected action
    if st.session_state["grade_action"] == "record":
        st.header("Record New Grades")
        with st.form("record_grades"):
            student = st.selectbox("Select Student", ["Student 1", "Student 2"])
            course = st.selectbox("Select Course", ["Mathematics", "Physics", "Chemistry"])
            grade = st.number_input("Grade", min_value=0.0, max_value=4.0, step=0.1)
            
            if st.form_submit_button("Submit Grade"):
                st.success("Grade recorded successfully!")

    elif st.session_state["grade_action"] == "view":
        st.header("Grade Records")
        # Add grade record display and search functionality

    elif st.session_state["grade_action"] == "analytics":
        st.header("Grade Analytics")
        # Add grade analytics and visualization

def main():
    SideBarLinks(show_home=True)
    show_grade_manager()

if __name__ == "__main__":
    main()