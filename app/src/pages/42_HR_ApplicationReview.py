import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_application_review():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("Application Review System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    st.divider()
    
    # Main operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Pending Applications", use_container_width=True):
            st.session_state["review_action"] = "pending"
            
    with col2:
        if st.button("Review History", use_container_width=True):
            st.session_state["review_action"] = "history"
            
    with col3:
        if st.button("Application Analytics", use_container_width=True):
            st.session_state["review_action"] = "analytics"

    st.divider()

    # Initialize action if not set
    if "review_action" not in st.session_state:
        st.session_state["review_action"] = None

    # Display different sections based on selected action
    if st.session_state["review_action"] == "pending":
        st.header("Pending Applications")
        # Example application review interface
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("Applicant: John Doe")
                st.write("Position: Software Developer Intern")
                st.write("Applied: 2023-11-20")
            with col2:
                if st.button("Accept", key="accept1"):
                    st.success("Application accepted!")
                if st.button("Reject", key="reject1"):
                    st.error("Application rejected")

    elif st.session_state["review_action"] == "history":
        st.header("Review History")
        # Add review history display

    elif st.session_state["review_action"] == "analytics":
        st.header("Application Analytics")
        # Add analytics display

def main():
    SideBarLinks(show_home=True)
    show_application_review()

if __name__ == "__main__":
    main()