import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_coop_records():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
        st.error("Please login as a Student to access this page.")
        st.stop()

    st.title("Co-op Experience Records")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/00_Student_Home.py")
    
    st.divider()
    
    # Main co-op operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Add Co-op Experience", use_container_width=True):
            st.session_state["coop_action"] = "add"
            
    with col2:
        if st.button("View Co-op History", use_container_width=True):
            st.session_state["coop_action"] = "view"
            
    with col3:
        if st.button("Co-op Insights", use_container_width=True):
            st.session_state["coop_action"] = "insights"

    st.divider()

    # Initialize co-op action if not set
    if "coop_action" not in st.session_state:
        st.session_state["coop_action"] = None

    # Display different sections based on selected action
    if st.session_state["coop_action"] == "add":
        st.header("Add New Co-op Experience")
        with st.form("coop_add"):
            company = st.text_input("Company Name")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            description = st.text_area("Experience Description")
            
            if st.form_submit_button("Submit"):
                st.success("Co-op experience added successfully!")

    elif st.session_state["coop_action"] == "view":
        st.header("Co-op History")
        # Add co-op history display

    elif st.session_state["coop_action"] == "insights":
        st.header("Co-op Insights")
        # Add insights and analytics display

def main():
    SideBarLinks(show_home=True)
    show_coop_records()

if __name__ == "__main__":
    main()
