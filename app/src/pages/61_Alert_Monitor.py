import streamlit as st
import requests
from datetime import datetime
from modules.nav import SideBarLinks

def format_date(date_str):
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

def main():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    st.title("Backup Management System")

    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/60_Maintenance_Home.py")

    # Create tabs
    tabs = st.tabs(["Manage Backups", "Create New Backup"])

    # Tab 1: Manage Backups
    with tabs[0]:
        st.subheader("Manage Backups")
        try:
            # Get database info for reference
            db_response = requests.get('http://web-api:4000/api/maintenance/databases')
            if db_response.status_code == 200:
                databases = {db['database_id']: db for db in db_response.json()}
            
            # Get backups
            backup_response = requests.get('http://web-api:4000/api/maintenance/backups')
            if backup_response.status_code == 200:
                backups = backup_response.json()
                if backups:
                    for i, backup in enumerate(backups):
                        with st.container():
                            # Get associated database info
                            db_id = backup.get('database_id')
                            db_info = databases.get(db_id, {}) if db_id else {}

                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**Type:** {backup.get('type', 'N/A')}")
                                st.write(f"**Schedule Type:** {backup.get('backup_type', 'N/A')}")
                                st.write(f"**Database:** {backup.get('database_name', 'N/A')}")
                                st.write(f"**Date:** {format_date(backup.get('backup_date', 'N/A'))}")
                                if backup.get('details'):
                                    st.write(f"**Details:** {backup.get('details')}")

                            with col2:
                                # Use unique keys for buttons
                                unique_id = f"{i}_{backup.get('database_id', '')}"
                                if st.button("View", key=f"view_{unique_id}"):
                                    st.json(backup)
                                if st.button("Delete", key=f"delete_{unique_id}"):
                                    try:
                                        delete_response = requests.delete(
                                            f"http://web-api:4000/api/maintenance/backups/{backup.get('database_id', '')}"
                                        )
                                        if delete_response.status_code == 200:
                                            st.success("Backup deleted successfully!")
                                            st.rerun()  # Updated from experimental_rerun
                                        else:
                                            st.error("Failed to delete backup")
                                    except Exception as e:
                                        st.error(f"Error deleting backup: {str(e)}")

                            st.divider()
                else:
                    st.info("No backups found")
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")

    # Tab 2: Create New Backup
    with tabs[1]:
        st.subheader("Create New Backup")
        
        # Get available databases
        try:
            db_response = requests.get('http://web-api:4000/api/maintenance/databases')
            if db_response.status_code == 200:
                databases = db_response.json()
                database_names = [db['name'] for db in databases]
            else:
                database_names = []
        except:
            database_names = []

        with st.form("backup_form", clear_on_submit=True):
            # Match the database schema fields
            selected_db = st.selectbox(
                "Select Database",
                options=database_names if database_names else ["No databases available"]
            )
            
            backup_type = st.selectbox(
                "Backup Type",
                options=["Full", "Incremental"]
            )
            
            schedule_type = st.selectbox(
                "Schedule Type",
                options=["Daily", "Weekly", "Monthly", "Manual"]
            )
            
            details = st.text_area(
                "Backup Details",
                placeholder="Enter any additional details about this backup"
            )

            submitted = st.form_submit_button("Create Backup")
            if submitted:
                try:
                    # Prepare data according to database schema
                    backup_data = {
                        "type": backup_type,
                        "backup_type": schedule_type,
                        "details": details,
                        "database_name": selected_db
                    }
                    
                    response = requests.post(
                        'http://web-api:4000/api/maintenance/backups',
                        json=backup_data
                    )
                    
                    if response.status_code == 201:
                        st.success("Backup created successfully!")
                        st.rerun()  # Updated from experimental_rerun
                    else:
                        st.error("Failed to create backup")
                except Exception as e:
                    st.error(f"Error creating backup: {str(e)}")

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()