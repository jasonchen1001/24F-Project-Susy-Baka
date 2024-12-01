import streamlit as st
from modules.nav import SideBarLinks
import logging
import pandas as pd
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_alerts(active_only=False):
    try:
        response = requests.get('http://web-api:4000/api/maintenance/alerts')
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            if active_only:
                return df[df['severity'] == 'High']
            return df
        else:
            st.error("Failed to load alerts")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading alerts: {str(e)}")
        st.error("Error connecting to server")
        return pd.DataFrame()

def show_alert_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    st.title("Alert Management System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/60_Maintenance_Home.py")
    
    st.divider()
    
    # Main alert operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("View Active Alerts", use_container_width=True):
            st.session_state["alert_action"] = "active"
            
    with col2:
        if st.button("Alert History", use_container_width=True):
            st.session_state["alert_action"] = "history"
            
    with col3:
        if st.button("Alert Settings", use_container_width=True):
            st.session_state["alert_action"] = "settings"

    st.divider()

    # Initialize alert action if not set
    if "alert_action" not in st.session_state:
        st.session_state["alert_action"] = None

    # Display different sections based on selected action
    if st.session_state["alert_action"] == "active":
        st.header("Active Alerts")
        df = load_alerts(active_only=True)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No active alerts")

    elif st.session_state["alert_action"] == "history":
        st.header("Alert History")
        df = load_alerts()
        if not df.empty:
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                severity_filter = st.multiselect(
                    'Filter by Severity:',
                    options=df['severity'].unique(),
                    default=[]
                )
            with col2:
                database_filter = st.multiselect(
                    'Filter by Database:',
                    options=df['database_name'].unique(),
                    default=[]
                )
            
            # Apply filters
            filtered_df = df
            if severity_filter:
                filtered_df = filtered_df[filtered_df['severity'].isin(severity_filter)]
            if database_filter:
                filtered_df = filtered_df[filtered_df['database_name'].isin(database_filter)]
            
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No alert history available")

    elif st.session_state["alert_action"] == "settings":
        st.header("Alert Settings")
        with st.form("alert_settings"):
            st.selectbox("Default Alert Severity", ["Low", "Medium", "High"])
            st.number_input("Alert Retention Period (days)", min_value=1, value=30)
            st.checkbox("Enable Email Notifications")
            st.text_input("Notification Email Addresses")
            
            if st.form_submit_button("Save Settings"):
                st.success("Alert settings saved successfully!")

def main():
    SideBarLinks(show_home=True)
    show_alert_manager()

if __name__ == "__main__":
    main()