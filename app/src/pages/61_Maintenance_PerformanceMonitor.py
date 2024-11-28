import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests
from datetime import datetime

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_backup_history():
    try:
        # Replace with your actual API endpoint
        response = requests.get('http://localhost:5000/api/system/backups')
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            st.error("Failed to load backup history")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading backup history: {str(e)}")
        st.error("Error connecting to server")
        return pd.DataFrame()

def show_backup_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    st.title("Backup Management System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/60_Maintenance_Home.py")
    
    st.divider()
    
    # Main backup operations in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Create New Backup", use_container_width=True):
            st.session_state["backup_action"] = "create"
            
    with col2:
        if st.button("View Backup History", use_container_width=True):
            st.session_state["backup_action"] = "history"
            
    with col3:
        if st.button("Backup Settings", use_container_width=True):
            st.session_state["backup_action"] = "settings"
    
    st.divider()
    
    # Initialize backup action if not set
    if "backup_action" not in st.session_state:
        st.session_state["backup_action"] = None
    
    # Handle different backup actions
    if st.session_state["backup_action"] == "create":
        st.header("Create New Backup")
        with st.form("create_backup"):
            backup_type = st.selectbox('Backup Type:', ['Full', 'Incremental'])
            schedule = st.selectbox('Schedule:', ['Daily', 'Weekly'])
            description = st.text_area('Description:')
            
            if st.form_submit_button("Create Backup"):
                try:
                    response = requests.post(
                        'http://localhost:5000/api/system/backups',
                        json={
                            'type': backup_type,
                            'schedule': schedule,
                            'description': description,
                            'date': datetime.now().strftime('%Y-%m-%d')
                        }
                    )
                    if response.status_code == 200:
                        st.success("Backup created successfully!")
                    else:
                        st.error("Failed to create backup")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    
    elif st.session_state["backup_action"] == "history":
        st.header("Backup History")
        df = load_backup_history()
        if not df.empty:
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                type_filter = st.multiselect(
                    'Filter by Type:',
                    options=df['type'].unique(),
                    default=[]
                )
            with col2:
                schedule_filter = st.multiselect(
                    'Filter by Schedule:',
                    options=df['schedule'].unique(),
                    default=[]
                )
                
            # Apply filters
            filtered_df = df
            if type_filter:
                filtered_df = filtered_df[filtered_df['type'].isin(type_filter)]
            if schedule_filter:
                filtered_df = filtered_df[filtered_df['schedule'].isin(schedule_filter)]
                
            # Display backups with delete option
            for idx, row in filtered_df.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Date:** {row.get('date', 'N/A')}")
                    st.write(f"**Type:** {row.get('type', 'N/A')}")
                    st.write(f"**Schedule:** {row.get('schedule', 'N/A')}")
                    if 'description' in row:
                        st.write(f"**Description:** {row['description']}")
                with col2:
                    if st.button('Delete', key=f'delete_{idx}'):
                        try:
                            response = requests.delete(
                                f'http://localhost:5000/api/system/backups/{row["id"]}'
                            )
                            if response.status_code == 200:
                                st.success("Backup deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete backup")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                st.divider()
                
    elif st.session_state["backup_action"] == "settings":
        st.header("Backup Settings")
        with st.form("backup_settings"):
            st.selectbox("Default Backup Type", ["Full", "Incremental"])
            st.selectbox("Default Schedule", ["Daily", "Weekly"])
            st.number_input("Retention Period (days)", min_value=1, value=30)
            st.text_input("Backup Location")
            
            if st.form_submit_button("Save Settings"):
                st.success("Settings saved successfully!")

def main():
    SideBarLinks(show_home=True)
    show_backup_manager()

if __name__ == "__main__":
    main()