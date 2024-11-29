import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests
from datetime import datetime

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_task_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    st.title("Task Management System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/60_Maintenance_Home.py")
    
    st.divider()
    
    # Main task operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Create New Task", use_container_width=True):
            st.session_state["task_action"] = "create"
            
    with col2:
        if st.button("View Tasks", use_container_width=True):
            st.session_state["task_action"] = "view"
            
    with col3:
        if st.button("Task Settings", use_container_width=True):
            st.session_state["task_action"] = "settings"

    st.divider()

    # Initialize task action if not set
    if "task_action" not in st.session_state:
        st.session_state["task_action"] = None

    # Display different sections based on selected action
    if st.session_state["task_action"] == "create":
        st.header("Create New Task")
        # Add your task creation form here

    elif st.session_state["task_action"] == "view":
        st.header("Task List")
        # Add your task list display logic here

    elif st.session_state["task_action"] == "settings":
        st.header("Task Settings")
        # Add your task settings logic here

def main():
    SideBarLinks(show_home=True)
    show_task_manager()

if __name__ == "__main__":
    main()