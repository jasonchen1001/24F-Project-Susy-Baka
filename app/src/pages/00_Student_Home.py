import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests

# Configure logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_student_metrics(user_id=1):
    """Load metrics for student dashboard display"""
    try:
        # Get student metrics
        response = requests.get(f"http://web-api:4000/student/{user_id}/metrics")
        if response.status_code == 200:
            metrics = response.json()
            active_applications = metrics.get('active_applications', 0)
            resume_versions = metrics.get('resume_versions', 0)
            latest_coop = metrics.get('latest_coop', 'None')
            return active_applications, resume_versions, latest_coop
        else:
            logger.error(f"API request failed with status code: {response.status_code}")
            return 0, 0, "None"
    except Exception as e:
        logger.error(f"Error loading metrics: {str(e)}")
        return 0, 0, "None"

def main():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
        st.error("Please login as a Student to access this page.")
        st.stop()

    st.title("Student Career Management")
    st.write(f"Welcome, {st.session_state.get('first_name')}!")
    st.divider()

    try:
        # Load student metrics with error handling
        metrics = load_student_metrics()
        if metrics is None:
            active_apps, resume_count, latest_coop = 0, 0, "None"
        else:
            active_apps, resume_count, latest_coop = metrics

        # Create layout with columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Quick Actions")
            if st.button("View Personal Information", use_container_width=True):
                st.switch_page("pages/01_Student_PersonalInfo.py")
            if st.button("Manage Resume", use_container_width=True):
                st.switch_page("pages/02_Student_ResumeManager.py")
            if st.button("Track Applications", use_container_width=True):
                st.switch_page("pages/03_Student_Applications.py")

        with col2:
            st.subheader("Your Career Overview")
            col2a, col2b, col2c = st.columns(3)
            with col2a:
                st.metric("Active Applications", active_apps)
            with col2b:
                st.metric("Resume Versions", resume_count)
            with col2c:
                st.metric("Latest Co-op", latest_coop)

            # Add status information
            st.write("---")
            st.write("### Profile Status")
            if all(v == 0 for v in [active_apps, resume_count]) and latest_coop == "None":
                st.warning("Profile needs to be updated")
            else:
                st.info("Profile is up to date")

        # Add recent updates
        st.write("---")
        st.write("### Recent Updates")
        st.write("""
        - New internship positions available
        - Resume builder updated
        - Application tracking system enhanced
        """)

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        st.error("An error occurred while loading the dashboard")

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()