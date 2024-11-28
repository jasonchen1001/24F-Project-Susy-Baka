import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_position_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("Internship Position Management")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    st.divider()
    
    # Main operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Post New Position", use_container_width=True):
            st.session_state["position_action"] = "post"
            
    with col2:
        if st.button("View Active Positions", use_container_width=True):
            st.session_state["position_action"] = "view"
            
    with col3:
        if st.button("Position Analytics", use_container_width=True):
            st.session_state["position_action"] = "analytics"

    st.divider()

    # Initialize action if not set
    if "position_action" not in st.session_state:
        st.session_state["position_action"] = None

    # Display different sections based on selected action
    if st.session_state["position_action"] == "post":
        st.header("Post New Position")
        with st.form("post_position"):
            title = st.text_input("Position Title")
            description = st.text_area("Description")
            requirements = st.text_area("Requirements")
            status = st.selectbox("Status", ["Active", "Inactive"])
            
            if st.form_submit_button("Post Position"):
                st.success("Position posted successfully!")

    elif st.session_state["position_action"] == "view":
        st.header("Active Positions")
        # Add position list and management functionality

    elif st.session_state["position_action"] == "analytics":
        st.header("Position Analytics")
        # Add analytics display

def main():
    SideBarLinks(show_home=True)
    show_position_manager()

if __name__ == "__main__":
    main()
