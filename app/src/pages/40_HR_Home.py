import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests

# Configure logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_dashboard_metrics():
    """Load metrics for dashboard display"""
    try:
        # Get position analytics
        response = requests.get("http://localhost:4000/hr/analytics/positions")
        if response.status_code == 200:
            analytics = response.json()
            total_positions = len(analytics)
            total_applications = sum(pos['total_applications'] for pos in analytics)
            pending_applications = sum(pos['pending'] for pos in analytics)
            return total_positions, total_applications, pending_applications
    except Exception as e:
        logger.error(f"Error loading metrics: {str(e)}")
        return 0, 0, 0

def main():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("HR Management System")
    st.write(f"Welcome, {st.session_state.get('first_name')}!")
    st.divider()

    # Load dashboard metrics
    positions, applications, pending = load_dashboard_metrics()

    # Create layout with columns
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Manage Internship Positions", use_container_width=True):
            st.switch_page("pages/41_HR_PositionManager.py")
        if st.button("Review Applications", use_container_width=True):
            st.switch_page("pages/42_HR_ApplicationReview.py")
        if st.button("Resume Screening", use_container_width=True):
            st.switch_page("pages/43_HR_ResumeScreen.py")

    with col2:
        st.write("### Recruitment Overview")
        st.metric("Active Positions", positions)
        st.metric("Total Applications", applications)
        st.metric("Pending Applications", pending)

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()