import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_maintenance_home():
    st.title('Maintenance Management System')
    
    # Check authentication
    if not st.session_state.get('authenticated') or st.session_state.get('role') != 'Maintenance_Staff':
        st.error('Please login as Maintenance Staff to access this page')
        st.stop()
        
    # Display welcome message
    st.write(f"Welcome, {st.session_state.get('first_name')}!")
    st.write("\n\n")
    
    # Create layout with columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### System Performance")
        if st.button("Monitor System Performance", use_container_width=True):
            st.switch_page("pages/61_Performance_Monitor.py")
            
        st.write("### Backup Management")
        if st.button("Manage Backups", use_container_width=True):
            st.switch_page("pages/62_Backup_Manager.py")
            
        st.write("### Alert Management")
        if st.button("Manage Alerts", use_container_width=True):
            st.switch_page("pages/63_Alert_Manager.py")
    
    with col2:
        st.write("### Maintenance Tasks")
        if st.button("Manage Tasks", use_container_width=True):
            st.switch_page("pages/64_Task_Manager.py")
            
        st.write("### Schema Management")
        if st.button("Manage Database Schema", use_container_width=True):
            st.switch_page("pages/65_Schema_Manager.py")
            
        st.write("### System Overview")
        st.metric("Active Alerts", "3")
        st.metric("Pending Tasks", "5")
        st.metric("Last Backup", "2 hours ago")

def main():
    SideBarLinks(show_home=True)
    show_maintenance_home()

if __name__ == "__main__":
    main()