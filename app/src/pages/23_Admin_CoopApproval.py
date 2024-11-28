import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_coop_approval():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "School_Admin":
        st.error("Please login as School Administrator to access this page.")
        st.stop()

    st.title("Co-op Approval Management")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/20_Admin_Home.py")
    
    st.divider()
    
    # Main operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Pending Approvals", use_container_width=True):
            st.session_state["approval_action"] = "pending"
            
    with col2:
        if st.button("Approval History", use_container_width=True):
            st.session_state["approval_action"] = "history"
            
    with col3:
        if st.button("Co-op Analytics", use_container_width=True):
            st.session_state["approval_action"] = "analytics"

    st.divider()

    # Initialize action if not set
    if "approval_action" not in st.session_state:
        st.session_state["approval_action"] = None

    # Display different sections based on selected action
    if st.session_state["approval_action"] == "pending":
        st.header("Pending Co-op Approvals")
        # Example pending approvals list
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("Student: John Doe")
                st.write("Company: Tech Corp")
                st.write("Duration: 3 months")
            with col2:
                if st.button("Approve", key="approve1"):
                    st.success("Co-op approved!")
                if st.button("Reject", key="reject1"):
                    st.error("Co-op rejected")

    elif st.session_state["approval_action"] == "history":
        st.header("Approval History")
        # Add approval history display

    elif st.session_state["approval_action"] == "analytics":
        st.header("Co-op Analytics")
        # Add analytics display

def main():
    SideBarLinks(show_home=True)
    show_coop_approval()

if __name__ == "__main__":
    main()