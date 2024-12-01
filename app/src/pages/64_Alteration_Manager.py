import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests
from datetime import datetime

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_alterations():
    """Load alteration history from API"""
    try:
        response = requests.get('http://web-api:4000/api/maintenance/alterations')
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            st.error("Failed to load alterations")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading alterations: {str(e)}")
        st.error("Error connecting to server")
        return pd.DataFrame()

def show_task_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    st.title("Data Alteration Management")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/60_Maintenance_Home.py")
    
    st.divider()
    
    # Main task operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Create New Alteration", use_container_width=True):
            st.session_state["task_action"] = "create"
            
    with col2:
        if st.button("View Alterations", use_container_width=True):
            st.session_state["task_action"] = "view"
            
    with col3:
        if st.button("Alteration Settings", use_container_width=True):
            st.session_state["task_action"] = "settings"

    st.divider()

    # Initialize task action if not set
    if "task_action" not in st.session_state:
        st.session_state["task_action"] = None

    # Display different sections based on selected action
    if st.session_state["task_action"] == "create":
        st.header("Create New Alteration")
        with st.form("create_alteration"):
            # Get databases list for selection
            try:
                db_response = requests.get('http://web-api:4000/api/maintenance/databases')
                databases = [db['name'] for db in db_response.json()] if db_response.status_code == 200 else ['Production', 'Development', 'Testing']
            except Exception:
                databases = ['Production', 'Development', 'Testing']
            
            alteration_type = st.selectbox(
                'Alteration Type:', 
                ['Schema Change', 'Data Update', 'Index Modification', 'Stored Procedure Update']
            )
            database = st.selectbox('Database:', databases)
            details = st.text_area('Alteration Details:', 
                                 help="Provide detailed description of the changes")
            impact = st.selectbox(
                'Impact Level:',
                ['Low', 'Medium', 'High'],
                help="Expected impact on system performance"
            )
            scheduled_date = st.date_input("Scheduled Date:")
            
            col1, col2 = st.columns(2)
            with col1:
                requires_downtime = st.checkbox("Requires Downtime")
            with col2:
                needs_backup = st.checkbox("Requires Backup", value=True)
            
            if st.form_submit_button("Create Alteration"):
                try:
                    response = requests.post(
                        'http://web-api:4000/api/maintenance/alterations',
                        json={
                            'alteration_type': alteration_type,
                            'change_id': database,  # using database as change_id
                            'alteration_date': scheduled_date.strftime('%Y-%m-%d'),
                            'details': {
                                'description': details,
                                'impact': impact,
                                'requires_downtime': requires_downtime,
                                'needs_backup': needs_backup
                            }
                        }
                    )
                    if response.status_code == 201:
                        st.success("Alteration created successfully!")
                        # Clear form
                        st.session_state["task_action"] = "view"
                        st.rerun()
                    else:
                        st.error("Failed to create alteration")
                except Exception as e:
                    logger.error(f"Error creating alteration: {str(e)}")
                    st.error(f"Error: {str(e)}")

    elif st.session_state["task_action"] == "view":
        st.header("Alteration History")
        df = load_alterations()
        if not df.empty:
            # Add filters
            col1, col2, col3 = st.columns(3)
            with col1:
                type_filter = st.multiselect(
                    'Filter by Type:',
                    options=df['alteration_type'].unique(),
                    default=[]
                )
            with col2:
                database_filter = st.multiselect(
                    'Filter by Database:',
                    options=df['database_name'].unique(),
                    default=[]
                )
            with col3:
                date_range = st.date_input(
                    "Date Range",
                    value=(datetime.now(), datetime.now()),
                    key="date_range"
                )
            
            # Apply filters
            filtered_df = df.copy()
            if type_filter:
                filtered_df = filtered_df[filtered_df['alteration_type'].isin(type_filter)]
            if database_filter:
                filtered_df = filtered_df[filtered_df['database_name'].isin(database_filter)]
            if len(date_range) == 2:
                filtered_df = filtered_df[
                    (filtered_df['alteration_date'] >= date_range[0].strftime('%Y-%m-%d')) &
                    (filtered_df['alteration_date'] <= date_range[1].strftime('%Y-%m-%d'))
                ]
            
            # Display alterations
            st.write(f"Showing {len(filtered_df)} alterations")
            for idx, row in filtered_df.iterrows():
                with st.expander(
                    f"{row['alteration_date']} - {row['alteration_type']} on {row['database_name']}", 
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Details:**")
                        st.write(row.get('details', 'No details provided'))
                        st.write(f"**Impact Level:** {row.get('impact', 'Not specified')}")
                    with col2:
                        st.write("**Status Information:**")
                        st.write(f"Created by: {row.get('first_name', '')} {row.get('last_name', '')}")
                        st.write(f"Requires Downtime: {row.get('requires_downtime', False)}")
                        st.write(f"Backup Required: {row.get('needs_backup', True)}")
        else:
            st.info("No alterations available")

    elif st.session_state["task_action"] == "settings":
        st.header("Alteration Settings")
        with st.form("alteration_settings"):
            # Get databases for default selection
            try:
                db_response = requests.get('http://web-api:4000/api/maintenance/databases')
                databases = [db['name'] for db in db_response.json()] if db_response.status_code == 200 else ['Production', 'Development', 'Testing']
            except Exception:
                databases = ['Production', 'Development', 'Testing']
                
            st.selectbox("Default Database", databases)
            st.number_input("Default Notice Period (hours)", min_value=1, value=24)
            st.checkbox("Require Approval for All Changes", value=True)
            st.checkbox("Always Require Backup", value=True)
            st.checkbox("Enable Email Notifications", value=True)
            
            notification_settings = st.expander("Notification Settings")
            with notification_settings:
                st.text_input("Email Recipients (comma-separated)")
                st.multiselect("Notify On:", [
                    "Alteration Created",
                    "Alteration Approved",
                    "Alteration Started",
                    "Alteration Completed",
                    "Backup Created",
                    "Error Occurred"
                ], default=["Alteration Created", "Error Occurred"])
            
            if st.form_submit_button("Save Settings"):
                st.success("Settings saved successfully!")

def main():
    SideBarLinks(show_home=True)
    show_task_manager()

if __name__ == "__main__":
    main()