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
        response = requests.get("http://web-api:4000/hr/analytics/positions")
        if response.status_code == 200:
            analytics = response.json()
            total_positions = len(analytics)
            total_applications = sum(pos.get('total_applications', 0) for pos in analytics)
            pending_applications = sum(pos.get('pending', 0) for pos in analytics)
            return total_positions, total_applications, pending_applications
        else:
            logger.error(f"API request failed with status code: {response.status_code}")
            return 0, 0, 0
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

    try:
        # Load dashboard metrics with error handling
        metrics = load_dashboard_metrics()
        if metrics is None:
            positions, applications, pending = 0, 0, 0
        else:
            positions, applications, pending = metrics

        # Create layout with columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Quick Actions")
            if st.button("Manage Internship Positions", use_container_width=True):
                st.switch_page("pages/41_HR_PositionManager.py")
            if st.button("Review Applications", use_container_width=True):
                st.switch_page("pages/42_HR_ApplicationReview.py")
            if st.button("Resume Screening", use_container_width=True):
                st.switch_page("pages/43_HR_ResumeScreen.py")

        with col2:
            st.subheader("Recruitment Overview")
            col2a, col2b, col2c = st.columns(3)
            with col2a:
                st.metric("Active Positions", positions)
            with col2b:
                st.metric("Total Applications", applications)
            with col2c:
                st.metric("Pending Applications", pending)

            # Add additional info or charts if needed
            st.write("---")
            st.write("### System Status")
            if all(v == 0 for v in [positions, applications, pending]):
                st.warning("Unable to connect to API")
            else:
                st.info("All systems operational")

        # Add some general information at the bottom
        st.write("---")
        st.write("### Recent Updates")
        st.write("""
        - New application review system implemented
        - Updated internship position templates
        - Enhanced resume screening capabilities
        """)

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        st.error("An error occurred while loading the dashboard")

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()