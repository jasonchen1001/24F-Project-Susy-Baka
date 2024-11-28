import streamlit as st
from modules.nav import SideBarLinks
import logging

# Configure Logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Page Title
st.title("Maintenance Management System")

# Description
st.write("Welcome to the Maintenance Management Dashboard!")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
    st.error("Please login as Maintenance Staff to access this page.")
    st.stop()

# Welcome Message
st.write(f"Welcome, {st.session_state.get('first_name')}!")
st.write("\n")

# Create layout with columns
col1, col2 = st.columns(2)

with col1:
    if st.button("Monitor System Performance", use_container_width=True):
        st.switch_page("pages/61_Maintenance_PerformanceMonitor.py")
            
    if st.button("Manage Backups", use_container_width=True):
        st.switch_page("pages/62_Maintenance_BackupManager.py")
            
    if st.button("Manage Alerts", use_container_width=True):
        st.switch_page("pages/63_Alert_Manager.py")

with col2:
    if st.button("Manage Tasks", use_container_width=True):
        st.switch_page("pages/64_Task_Manager.py")
            
    if st.button("Manage Database Schema", use_container_width=True):
        st.switch_page("pages/65_Schema_Manager.py")
            
    st.write("### System Overview")
    st.metric("Active Alerts", "3")
    st.metric("Pending Tasks", "5")
    st.metric("Last Backup", "2 hours ago")