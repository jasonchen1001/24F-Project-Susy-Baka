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

# Initialize Session States for Expansion Panels
if "performance_expanded" not in st.session_state:
    st.session_state.performance_expanded = False
if "backup_expanded" not in st.session_state:
    st.session_state.backup_expanded = False

# Navigation Buttons
if st.button("Monitor System Performance"):
    st.session_state.performance_expanded = not st.session_state.performance_expanded

if st.session_state.performance_expanded:
    if st.button("View Performance Dashboard"):
        st.session_state["page"] = "61_Maintenance_PerformanceMonitor"
        st.rerun()
    if st.button("Performance History"):
        st.session_state["page"] = "61_Maintenance_PerformanceMonitor"
        st.rerun()

if st.button("Manage Backups"):
    st.session_state.backup_expanded = not st.session_state.backup_expanded

if st.session_state.backup_expanded:
    if st.button("Create New Backup"):
        st.session_state["page"] = "62_Maintenance_BackupManager"
        st.rerun()
    if st.button("View Backup History"):
        st.session_state["page"] = "62_Maintenance_BackupManager"
        st.rerun()

if st.button("Manage Alerts"):
    st.session_state["page"] = "63_Alert_Manager"
    st.rerun()

if st.button("Manage Tasks"):
    st.session_state["page"] = "64_Task_Manager"
    st.rerun()

if st.button("Manage Database Schema"):
    st.session_state["page"] = "65_Schema_Manager"
    st.rerun()

# Metrics Section
st.write("### System Overview")
st.metric("Active Alerts", "3")
st.metric("Pending Tasks", "5")
st.metric("Last Backup", "2 hours ago")
