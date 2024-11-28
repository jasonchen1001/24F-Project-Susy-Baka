import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_student_records():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "School_Admin":
        st.error("Please login as School Administrator to access this page.")
        st.stop()

    st.title("Student Records Management")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/20_Admin_Home.py")
    
    st.divider()
    
    # Main operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("View Student Records", use_container_width=True):
            st.session_state["records_action"] = "view"
            
    with col2:
        if st.button("Add New Student", use_container_width=True):
            st.session_state["records_action"] = "add"
            
    with col3:
        if st.button("Student Statistics", use_container_width=True):
            st.session_state["records_action"] = "stats"

    st.divider()

    # Initialize action if not set
    if "records_action" not in st.session_state:
        st.session_state["records_action"] = None

    # Display different sections based on selected action
    if st.session_state["records_action"] == "view":
        st.header("Student Records")
        # Add search/filter options
        search = st.text_input("Search by Name or ID")
        
        # Example student list
        if search:
            st.write("Search results will be shown here")
            # Add your search logic here
            
    elif st.session_state["records_action"] == "add":
        st.header("Add New Student")
        with st.form("add_student"):
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            if st.form_submit_button("Add Student"):
                st.success("Student added successfully!")

    elif st.session_state["records_action"] == "stats":
        st.header("Student Statistics")
        # Add statistics display here

def main():
    SideBarLinks(show_home=True)
    show_student_records()

if __name__ == "__main__":
    main()