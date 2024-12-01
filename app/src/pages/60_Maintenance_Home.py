import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests
from datetime import datetime

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def format_date(date_str):
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

def load_metrics():
    """Load metrics from API endpoints"""
    try:
        metrics = {
            'active_alerts': 0,
            'pending_alterations': 0,
            'latest_backup': 'No backups',
            'total_databases': 0
        }
        
        # Get alerts
        alert_response = requests.get('http://web-api:4000/api/maintenance/alerts')
        if alert_response.status_code == 200:
            alerts = alert_response.json()
            metrics['active_alerts'] = len([a for a in alerts if a.get('severity') == 'High'])
        
        # Get alterations
        alteration_response = requests.get('http://web-api:4000/api/maintenance/alterations')
        if alteration_response.status_code == 200:
            alterations = alteration_response.json()
            metrics['pending_alterations'] = len(alterations)
        
        # Get backups
        backup_response = requests.get('http://web-api:4000/api/maintenance/backups')
        if backup_response.status_code == 200:
            backups = backup_response.json()
            if backups:
                metrics['latest_backup'] = format_date(backups[0].get('backup_date', 'Unknown'))
        
        # Get database count
        db_response = requests.get('http://web-api:4000/api/maintenance/databases')
        if db_response.status_code == 200:
            databases = db_response.json()
            metrics['total_databases'] = len(databases)
        
        return metrics
    except requests.exceptions.RequestException as e:
        logger.error(f"Error loading metrics: {str(e)}")
        return {
            'active_alerts': 'Error',
            'pending_alterations': 'Error',
            'latest_backup': 'Error',
            'total_databases': 'Error'
        }

def maintenance_layout():
    """Create main navigation and dashboard layout"""
    # Create two columns for navigation buttons
    col1, col2 = st.columns(2)

    with col1:
        st.page_link("pages/61_Alert_Monitor.py", 
                    label="Monitor System Alerts", 
                    use_container_width=True)
        st.page_link("pages/62_Backup_Manager.py", 
                    label="Manage Backups", 
                    use_container_width=True)
        st.page_link("pages/63_Alert_History.py", 
                    label="View Alert History", 
                    use_container_width=True)

    with col2:
        st.page_link("pages/64_Alteration_Manager.py", 
                    label="Data Alterations", 
                    use_container_width=True)
        st.page_link("pages/65_Database_Manager.py", 
                    label="Manage Database Schema", 
                    use_container_width=True)
            
    # System Overview Section
    st.write("### System Overview")
    
    # Load metrics with error handling
    with st.spinner("Loading system metrics..."):
        try:
            metrics = load_metrics()
            
            # Create a grid of metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("🔔 High Priority Alerts", 
                         metrics['active_alerts'])
                st.metric("📝 Pending Alterations", 
                         metrics['pending_alterations'])
            
            with col2:
                st.metric("💾 Last Backup", 
                         metrics['latest_backup'])
                st.metric("🗄️ Total Databases", 
                         metrics['total_databases'])
                
        except Exception as e:
            st.error(f"Error loading system metrics: {str(e)}")
            logger.error(f"Error in maintenance_layout: {str(e)}")

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
    
    # Add helpful tooltips in sidebar
    st.sidebar.info("""
    💡 Quick Links:
    - Monitor Alerts: View and manage system alerts
    - Manage Backups: Schedule and review backups
    - Alert History: View historical alerts
    - Data Alterations: Track database changes
    - Database Schema: Manage database structure
    """)

if __name__ == "__main__":
    main()