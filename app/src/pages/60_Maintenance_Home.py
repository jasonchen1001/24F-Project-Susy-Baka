import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function to fetch data from an API
def fetch_data(url):
    """Fetch data from a given API endpoint."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        st.error(f"Error fetching data: {e}")
        return None

# Main function
def main():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    st.title("Maintenance Management System")
    st.write(f"Welcome, {st.session_state.get('first_name', 'Maintenance Staff')}!")
    st.divider()

    # Layout with columns for navigation and information
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quick Actions")
        if st.button("Monitor Alerts", use_container_width=True):
            st.switch_page("pages/61_Alert_Monitor.py")
        if st.button("Manage Alterations", use_container_width=True):
            st.switch_page("pages/62_Data_Alteration_Manager.py")
        if st.button("Backup History", use_container_width=True):
            st.switch_page("pages/63_Backup_History.py")

    with col2:
        st.subheader("System Overview")
        st.write("""
        The Maintenance Management Portal allows you to:
        - Monitor system alerts and take necessary actions
        - Manage data alterations and update records
        - View and manage backup history for databases
        Select an option from the Quick Actions menu to get started.
        """)

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()
