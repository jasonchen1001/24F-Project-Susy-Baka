import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API 基础 URL
API_BASE_URL = "http://web-api:4000/maintenance_staff"

def fetch_backups():
    """获取备份历史"""
    try:
        response = requests.get(f"{API_BASE_URL}/backups")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching backups: {str(e)}")
        return None

def add_backup(database_id, backup_type, backup_date, details):
    """添加新的备份记录"""
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
    """更新备份记录"""
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
    """删除备份记录"""
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

def main():
    st.title("Backup History Management")
    st.write("Manage backup history for databases.")

    # 创建 tabs
    tab1, tab2 = st.tabs(["View and Edit", "Add and Delete"])

    # 获取备份历史
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
            selected_backup = st.selectbox(
                "Select Backup to Edit",
                options=df["database_id"].tolist(),
                format_func=lambda x: f"Database: {df[df['database_id']==x]['database_name'].iloc[0]} ({x})"
            )

            if selected_backup:
                backup_data = df[df["database_id"] == selected_backup].iloc[0]
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
                            selected_backup,
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
            if backups:
                df = pd.DataFrame(backups)
                with st.form("add_backup_form"):
                    selected_db = st.selectbox(
                        "Select Database",
                        options=df["database_id"].unique(),
                        format_func=lambda x: f"{df[df['database_id']==x]['database_name'].iloc[0]} ({x})"
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
                st.info("No backups available.")
        
        # Column 2: Delete Backup
        with col2:
            if backups:
                st.subheader("Delete Backup")
                delete_id = st.selectbox(
                    "Select Backup to Delete",
                    options=df["database_id"].tolist(),
                    format_func=lambda x: f"Database: {df[df['database_id']==x]['database_name'].iloc[0]} ({x})"
                )
                
                col_1, col_2 = st.columns([1, 3])
                with col_1:
                    if st.button("Delete", type="primary"):
                        if st.checkbox("Confirm deletion"):
                            delete_backup(delete_id)

if __name__ == "__main__":
    main()