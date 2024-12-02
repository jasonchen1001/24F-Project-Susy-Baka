import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests
from datetime import datetime

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def format_date(date_str):
    """Format date string to readable format"""
    try:
        if pd.isna(date_str):
            return "N/A"
        date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

def load_databases():
    """Load database information with related counts"""
    try:
        response = requests.get('http://web-api:4000/api/maintenance/databases')
        if response.status_code == 200:
            databases = response.json()
            
            # Convert to DataFrame and handle the data
            df = pd.DataFrame(databases)
            
            # Ensure all required columns exist
            required_columns = ['database_id', 'name', 'version', 'type', 'last_update', 'staff_name']
            for col in required_columns:
                if col not in df.columns:
                    df[col] = 'N/A'
            
            # Format dates
            if 'last_update' in df.columns:
                df['last_update'] = df['last_update'].apply(format_date)
            
            return df
        else:
            st.error("Failed to load database information")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading databases: {str(e)}")
        st.error("Error connecting to server")
        return pd.DataFrame()

def show_schema_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    st.title("Database Schema Management")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/60_Maintenance_Home.py")
    
    st.divider()
    
    # Main schema operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("View Databases", use_container_width=True):
            st.session_state["schema_action"] = "view"
            
    with col2:
        if st.button("Database Statistics", use_container_width=True):
            st.session_state["schema_action"] = "stats"
            
    with col3:
        if st.button("Schema History", use_container_width=True):
            st.session_state["schema_action"] = "history"

    st.divider()

    # Initialize schema action if not set
    if "schema_action" not in st.session_state:
        st.session_state["schema_action"] = "view"  # Default to view

    # Display different sections based on selected action
    if st.session_state["schema_action"] == "view":
        st.header("Database Information")
        df = load_databases()
        if not df.empty:
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                type_filter = st.multiselect(
                    'Filter by Type:',
                    options=sorted(df['type'].unique()),
                    default=[]
                )
            with col2:
                version_filter = st.multiselect(
                    'Filter by Version:',
                    options=sorted(df['version'].unique()),
                    default=[]
                )
            
            # Apply filters
            filtered_df = df.copy()
            if type_filter:
                filtered_df = filtered_df[filtered_df['type'].isin(type_filter)]
            if version_filter:
                filtered_df = filtered_df[filtered_df['version'].isin(version_filter)]
            
            # Display each database entry
            for _, row in filtered_df.iterrows():
                with st.expander(f"Database: {row['name']}", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Database Details:**")
                        st.write(f"Name: {row['name']}")
                        st.write(f"Type: {row['type']}")
                        st.write(f"Version: {row['version']}")
                        st.write(f"Last Update: {row['last_update']}")
                    with col2:
                        st.write("**Additional Information:**")
                        st.write(f"Managed by: {row['staff_name']}")
                        
                        # Get related counts
                        try:
                            alerts_response = requests.get(f"http://web-api:4000/api/maintenance/alerts?database_id={row['database_id']}")
                            alterations_response = requests.get(f"http://web-api:4000/api/maintenance/alterations?database_id={row['database_id']}")
                            
                            alerts_count = len(alerts_response.json()) if alerts_response.status_code == 200 else 0
                            alterations_count = len(alterations_response.json()) if alterations_response.status_code == 200 else 0
                            
                            st.write(f"Active Alerts: {alerts_count}")
                            st.write(f"Recent Alterations: {alterations_count}")
                        except:
                            st.write("Count information unavailable")
                    
                    st.divider()
        else:
            st.info("No database information available")

    elif st.session_state["schema_action"] == "stats":
        st.header("Database Statistics")
        df = load_databases()
        if not df.empty:
            # Overall statistics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Databases", len(df))
                st.metric("Database Types", len(df['type'].unique()))
            with col2:
                st.write("**Database Types Distribution:**")
                type_counts = df['type'].value_counts()
                for db_type, count in type_counts.items():
                    st.write(f"- {db_type}: {count}")
            
            # Show most recent updates
            st.subheader("Recent Updates")
            recent_updates = df.sort_values('last_update', ascending=False).head(5)
            for _, row in recent_updates.iterrows():
                st.write(f"- {row['name']}: {row['last_update']}")
        else:
            st.info("No statistics available")

    elif st.session_state["schema_action"] == "history":
        st.header("Schema Change History")
        try:
            history_response = requests.get('http://web-api:4000/api/maintenance/alterations')
            if history_response.status_code == 200:
                changes = history_response.json()
                for change in changes:
                    if change.get('alteration_type') == 'Schema Update':
                        st.write(f"**Date:** {format_date(change.get('alteration_date'))}")
                        st.write(f"**Database:** {change.get('database_name')}")
                        st.write(f"**Type:** {change.get('alteration_type')}")
                        st.divider()
            else:
                st.info("No schema changes found")
        except Exception as e:
            st.error(f"Error loading schema history: {str(e)}")

def main():
    SideBarLinks(show_home=True)
    show_schema_manager()

if __name__ == "__main__":
    main()