import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_databases():
    try:
        response = requests.get('http://web-api:4000/api/maintenance/databases')
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
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
        st.session_state["schema_action"] = None

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
                    options=df['type'].unique(),
                    default=[]
                )
            with col2:
                version_filter = st.multiselect(
                    'Filter by Version:',
                    options=df['version'].unique(),
                    default=[]
                )
            
            # Apply filters
            filtered_df = df
            if type_filter:
                filtered_df = filtered_df[filtered_df['type'].isin(type_filter)]
            if version_filter:
                filtered_df = filtered_df[filtered_df['version'].isin(version_filter)]
            
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No database information available")

    elif st.session_state["schema_action"] == "stats":
        st.header("Database Statistics")
        df = load_databases()
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Databases", len(df))
                st.metric("Active Alerts", df['alert_count'].sum())
            with col2:
                st.metric("Total Alterations", df['alteration_count'].sum())
                st.metric("Latest Update", df['last_update'].max())
        else:
            st.info("No statistics available")

    elif st.session_state["schema_action"] == "history":
        st.header("Schema Change History")
        # This would typically show a history of schema changes
        # You could implement this by tracking alterations of type 'schema_change'
        st.info("Schema history tracking coming soon")

def main():
    SideBarLinks(show_home=True)
    show_schema_manager()

if __name__ == "__main__":
    main()