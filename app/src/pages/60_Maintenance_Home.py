import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests

# Configure Logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_metrics():
    """Load metrics from API endpoints"""
    try:
        # Get alert count
        alert_response = requests.get('http://web-api:4000/api/maintenance/alerts')
        active_alerts = len([a for a in alert_response.json() if a['severity'] == 'High']) if alert_response.status_code == 200 else "N/A"
        
        # Get alteration count
        alteration_response = requests.get('http://web-api:4000/api/maintenance/alterations')
        pending_alterations = len(alteration_response.json()) if alteration_response.status_code == 200 else "N/A"
        
        # Get latest backup
        backup_response = requests.get('http://web-api:4000/api/maintenance/backups')
        if backup_response.status_code == 200:
            backups = backup_response.json()
            latest_backup = backups[0]['backup_date'] if backups else "No backups" 
        else:
            latest_backup = "N/A"
            
        return active_alerts, pending_alterations, latest_backup
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error loading metrics: {str(e)}")
        return "Error", "Error", "Error"

def maintenance_layout():
    """Create main navigation and dashboard layout"""
    col1, col2 = st.columns(2)

    with col1:
        st.page_link("pages/61_Alert_Monitor.py", label="Monitor System Alerts", use_container_width=True)
        st.page_link("pages/62_Backup_Manager.py", label="Manage Backups", use_container_width=True)
        st.page_link("pages/63_Alert_History.py", label="View Alert History", use_container_width=True)

    with col2:
        st.page_link("pages/64_Alteration_Manager.py", label="Data Alterations", use_container_width=True)
        st.page_link("pages/65_Database_Manager.py", label="Manage Database Schema", use_container_width=True)
            
        st.write("### System Overview")
    
        # Load live metrics
        with st.spinner("Loading metrics..."):
            active_alerts, pending_alterations, latest_backup = load_metrics()
        
        # Display metrics with icons
        st.metric("🔔 High Priority Alerts", active_alerts)
        st.metric("📝 Pending Alterations", pending_alterations)
        st.metric("💾 Last Backup", latest_backup)

def main():
    # Page Title
    st.title("Maintenance Management System")

    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Maintenance_Staff":
        st.error("Please login as Maintenance Staff to access this page.")
        st.stop()

    # Welcome Message
    st.write(f"Welcome, {st.session_state.get('first_name')}!")
    st.write("\n")
    
    # Display main layout
    maintenance_layout()
    


if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()