import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_alert_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    st.title("Alert Management System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/60_Maintenance_Home.py")
    
    st.divider()
    
    # Main alert operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("View Active Alerts", use_container_width=True):
            st.session_state["alert_action"] = "active"
            
    with col2:
        if st.button("Alert History", use_container_width=True):
            st.session_state["alert_action"] = "history"
            
    with col3:
        if st.button("Alert Settings", use_container_width=True):
            st.session_state["alert_action"] = "settings"

    st.divider()

    # Initialize alert action if not set
    if "alert_action" not in st.session_state:
        st.session_state["alert_action"] = None

    # Display different sections based on selected action
    if st.session_state["alert_action"] == "active":
        st.header("Active Alerts")
        # Add your active alerts display logic here

    elif st.session_state["alert_action"] == "history":
        st.header("Alert History")
        # Add your alert history display logic here

    elif st.session_state["alert_action"] == "settings":
        st.header("Alert Settings")
        # Add your alert settings logic here

def main():
    SideBarLinks(show_home=True)
    show_alert_manager()

if __name__ == "__main__":
    main()