import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_BASE_URL = "http://web-api:4000/maintenance_staff"

# Return to Home button
if st.button("← Back to Home"):
    st.switch_page("pages/60_Maintenance_Home.py")
    
def fetch_backups():
    try:
        response = requests.get(f"{API_BASE_URL}/backups")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching backups: {str(e)}")
        return None

def add_backup(database_id, backup_type, backup_date, details):
    try:
        response = requests.post(
            f"{API_BASE_URL}/backups",
            json={
                "database_id": database_id,
                "type": backup_type,
                "backup_date": backup_date,
                "details": details
            }
        )
        if response.status_code == 200:
            st.success("Backup added successfully!")
            st.rerun()
        else:
            st.error("Failed to add backup. Please try again.")
            if response.text:
                st.error(f"Error details: {response.text}")
    except Exception as e:
        st.error(f"Error adding backup: {str(e)}")

def update_backup(backup_id, backup_type, backup_date, details):

    try:
        response = requests.put(
            f"{API_BASE_URL}/backups/{backup_id}",
            json={
                "type": backup_type,
                "backup_date": backup_date,
                "details": details
            }
        )
        if response.status_code == 200:
            st.success("Backup updated successfully!")
            st.rerun()
        else:
            st.error("Failed to update backup. Please try again.")
            if response.text:
                st.error(f"Error details: {response.text}")
    except Exception as e:
        st.error(f"Error updating backup: {str(e)}")

def delete_backup(backup_id):

    try:
        response = requests.delete(f"{API_BASE_URL}/backups/{backup_id}")
        if response.status_code == 200:
            st.success("Backup deleted successfully!")
            st.rerun()
        else:
            st.error("Failed to delete backup. Please try again.")
            if response.text:
                st.error(f"Error details: {response.text}")
    except Exception as e:
        st.error(f"Error deleting backup: {str(e)}")

def format_backup_display(backup):
    date_str = backup['backup_date']
    try:
        
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT")
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
    except:
        formatted_date = date_str

    return f"Database: {backup['database_name']} | Type: {backup['type']} | Date: {formatted_date}"

def main():
    st.title("Backup History Management")
    st.write("Manage backup history for databases.")

    tab1, tab2 = st.tabs(["View and Edit", "Add and Delete"])

    backups = fetch_backups()

    # Tab 1: View and Edit
    with tab1:
        if backups:
            st.subheader("Current Backups")
            df = pd.DataFrame(backups)
            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True
            )

            st.subheader("Edit Backup")
         
            backup_options = [
                {
                    'id': backup.get('backup_id', backup['database_id']),
                    'display': format_backup_display(backup),
                    'data': backup
                }
                for backup in backups
            ]

            selected_backup_data = st.selectbox(
                "Select Backup to Edit",
                options=backup_options,
                format_func=lambda x: x['display']
            )

            if selected_backup_data:
                backup_data = selected_backup_data['data']
                with st.form("edit_backup_form"):
                    backup_type = st.selectbox(
                        "Backup Type",
                        options=["Full", "Incremental", "Differential"],
                        index=["Full", "Incremental", "Differential"].index(backup_data["type"])
                    )
                    
                    current_date = datetime.strptime(
                        backup_data["backup_date"], 
                        "%a, %d %b %Y %H:%M:%S GMT"
                    ).strftime("%Y-%m-%d")
                    
                    backup_date = st.date_input(
                        "Backup Date",
                        value=datetime.strptime(current_date, "%Y-%m-%d")
                    )
                    
                    details = st.text_area(
                        "Details",
                        value=backup_data["details"]
                    )
                    
                    if st.form_submit_button("Update Backup"):
                        update_backup(
                            selected_backup_data['id'],
                            backup_type,
                            backup_date.strftime("%Y-%m-%d"),
                            details
                        )
        else:
            st.info("No backups available.")

    # Tab 2: Add and Delete
    with tab2:
        col1, col2 = st.columns(2)
        
        # Column 1: Add New Backup
        with col1:
            st.subheader("Add New Backup")
            
            input_method = st.radio(
                "Choose input method",
                ["Select from existing database", "Manual entry"],
                key="input_method"
            )
            
            if input_method == "Select from existing database":
                if backups:
                    df = pd.DataFrame(backups)
                    with st.form("add_backup_form_select"):
                        unique_dbs = df.drop_duplicates(subset=['database_id', 'database_name'])
                        selected_db = st.selectbox(
                            "Select Database",
                            options=unique_dbs["database_id"].tolist(),
                            format_func=lambda x: f"{unique_dbs[unique_dbs['database_id']==x]['database_name'].iloc[0]} ({x})"
                        )
                        
                        backup_type = st.selectbox(
                            "Backup Type",
                            options=["Full", "Incremental", "Differential"]
                        )
                        
                        backup_date = st.date_input("Backup Date")
                        details = st.text_area("Details", value="Regular scheduled backup")
                        
                        if st.form_submit_button("Add Backup"):
                            add_backup(
                                selected_db,
                                backup_type,
                                backup_date.strftime("%Y-%m-%d"),
                                details
                            )
                else:
                    st.info("No existing databases available.")
            
            else:  # Manual entry
                with st.form("add_backup_form_manual"):
                    database_id = st.number_input("Database ID", min_value=1, step=1)
                    database_name = st.text_input("Database Name")
                    backup_type = st.selectbox(
                        "Backup Type",
                        options=["Full", "Incremental", "Differential"]
                    )
                    backup_date = st.date_input("Backup Date")
                    details = st.text_area("Details", value="Manual backup entry")
                    
                    if st.form_submit_button("Add Manual Backup"):
                        add_backup(
                            database_id,
                            backup_type,
                            backup_date.strftime("%Y-%m-%d"),
                            details
                        )
        
        # Column 2: Delete Backup
        with col2:
            if backups:
                st.subheader("Delete Backup")
                
                backup_options = [
                    {
                        'id': backup.get('backup_id', backup['database_id']),
                        'display': format_backup_display(backup),
                        'data': backup
                    }
                    for backup in backups
                ]
                
                selected_backup = st.selectbox(
                    "Select Backup to Delete",
                    options=backup_options,
                    format_func=lambda x: x['display'],
                    key="delete_backup_select"
                )
                
                if selected_backup:
                    backup_data = selected_backup['data']
                    
                    st.write("**Backup Details:**")
                    st.write(f"Database: {backup_data['database_name']}")
                    st.write(f"Backup Type: {backup_data['type']}")
                    st.write(f"Backup Date: {backup_data['backup_date']}")
                    st.write(f"Details: {backup_data['details']}")
                    
                    confirm = st.checkbox("I confirm that I want to delete this specific backup")
                    if confirm:
                        if st.button("Delete Selected Backup", type="primary"):
                            delete_backup(selected_backup['id'])

if __name__ == "__main__":
    main()