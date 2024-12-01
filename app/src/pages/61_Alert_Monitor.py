import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page config
st.title("Backup Management System")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
    st.error("Please login as Maintenance Staff to access this page.")
    st.stop()

# Tabs for functionality
tabs = st.tabs(["Manage Backups", "Create New Backup"])

# Tab 1: Manage Backups
with tabs[0]:
    st.subheader("Manage Backups")
    try:
        response = requests.get("http://web-api:4000/api/maintenance/backups")
        response.raise_for_status()  # Automatically raise error for HTTP issues

        backups = response.json()
        if backups:
            for backup in backups:
                with st.container():
                    st.write(f"**Type:** {backup.get('type', 'N/A')}")
                    st.write(f"**Backup Type:** {backup.get('backup_type', 'N/A')}")
                    st.write(f"**Details:** {backup.get('details', 'No details provided')}")
                    st.write(f"**Database:** {backup.get('database_name', 'N/A')}")
                    st.write(f"**Date:** {backup.get('backup_date', 'N/A')}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("View Details", key=f"view_{backup.get('database_id', '')}"):
                            st.info(f"Full backup details:\n{backup}")
                    with col2:
                        if st.button("Delete", key=f"delete_{backup.get('database_id', '')}"):
                            try:
                                delete_response = requests.delete(
                                    f"http://web-api:4000/api/maintenance/backups/{backup.get('database_id', '')}"
                                )
                                if delete_response.status_code == 200:
                                    st.success("Backup deleted successfully!")
                                    st.experimental_rerun()
                                else:
                                    st.error("Failed to delete backup.")
                            except Exception as e:
                                st.error(f"Error: {e}")
                    st.write("---")
        else:
            st.info("No backups found.")
    except Exception as e:
        st.error(f"Failed to load backups: {e}")

# Tab 2: Create New Backup
with tabs[1]:
    st.subheader("Create New Backup")
    with st.form("create_backup_form"):
        backup_type = st.selectbox("Backup Type", ["Full", "Incremental", "Differential"])
        backup_schedule = st.selectbox("Backup Type", ["Daily", "Weekly", "Monthly", "Manual"])
        details = st.text_area("Backup Details")

        if st.form_submit_button("Create Backup"):
            try:
                response = requests.post(
                    "http://web-api:4000/api/maintenance/backups",
                    json={
                        "type": backup_type,
                        "backup_type": backup_schedule,  # Changed to match database field
                        "details": details,
                        "description": details  # For backwards compatibility
                    }
                )
                if response.status_code == 201:
                    st.success("Backup created successfully!")
                    st.experimental_rerun()  # Refresh the page to show new backup
                else:
                    st.error(f"Failed to create backup. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error creating backup: {e}")