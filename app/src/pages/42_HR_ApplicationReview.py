import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests
from datetime import datetime

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_application_review():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("Application Review System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    st.divider()
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Pending Applications", "Review History", "Analytics"])
    
    # Tab 1: Pending Applications
    with tab1:
        try:
            with st.spinner("Loading pending applications..."):
                response = requests.get("http://web-api:4000/hr/applications", params={"status": "Pending"})
                if response.status_code == 200:
                    applications = response.json()
                    
                    if not applications:
                        st.info("No pending applications to review.")
                    
                    for app in applications:
                        with st.container():
                            st.write(f"### Application #{app['application_id']}")
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.write(f"**Applicant:** {app['full_name']}")
                                st.write(f"**Email:** {app['email']}")
                                st.write(f"**Position:** {app['position_title']}")
                                st.write(f"**Applied:** {app['sent_on']}")
                                
                            with col2:
                                if st.button("Accept", key=f"accept_{app['application_id']}", type="primary"):
                                    with st.spinner("Processing..."):
                                        response = requests.put(
                                            f"http://web-api:4000/hr/applications/{app['application_id']}",
                                            json={"status": "Accepted"}
                                        )
                                        if response.status_code == 200:
                                            st.success("Application accepted!")
                                            st.rerun()
                                
                                if st.button("Reject", key=f"reject_{app['application_id']}", type="secondary"):
                                    with st.spinner("Processing..."):
                                        response = requests.put(
                                            f"http://web-api:4000/hr/applications/{app['application_id']}",
                                            json={"status": "Rejected"}
                                        )
                                        if response.status_code == 200:
                                            st.success("Application rejected!")
                                            st.rerun()
                            
                            st.divider()
                else:
                    st.error("Failed to load applications")
        except Exception as e:
            st.error(f"Error loading applications: {str(e)}")
    
    # Tab 2: Review History
    with tab2:
        try:
            with st.spinner("Loading application history..."):
                response = requests.get("http://web-api:4000/hr/applications", params={"status": "all"})
                if response.status_code == 200:
                    applications = response.json()
                    
                    # Create filters
                    status_filter = st.selectbox(
                        "Filter by Status",
                        ["All", "Accepted", "Rejected", "Pending"]
                    )
                    
                    filtered_apps = [
                        app for app in applications
                        if status_filter == "All" or app['status'] == status_filter
                    ]
                    
                    if filtered_apps:
                        # Display applications in a table
                        st.write("### Application History")
                        app_data = {
                            "Applicant": [app['full_name'] for app in filtered_apps],
                            "Position": [app['position_title'] for app in filtered_apps],
                            "Applied Date": [app['sent_on'] for app in filtered_apps],
                            "Status": [app['status'] for app in filtered_apps]
                        }
                        st.dataframe(app_data, use_container_width=True)
                    else:
                        st.info("No applications found with selected filters.")
                else:
                    st.error("Failed to load application history")
        except Exception as e:
            st.error(f"Error loading review history: {str(e)}")
    
    # Tab 3: Analytics
    with tab3:
        try:
            with st.spinner("Loading analytics..."):
                response = requests.get("http://web-api:4000/hr/analytics/positions")
                if response.status_code == 200:
                    analytics = response.json()
                    
                    total_applications = sum(pos.get('total_applications', 0) for pos in analytics)
                    total_accepted = sum(pos.get('accepted', 0) for pos in analytics)
                    total_rejected = sum(pos.get('rejected', 0) for pos in analytics)
                    
                    # Display overall metrics
                    st.write("### Overall Application Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Applications", total_applications)
                    with col2:
                        acceptance_rate = (total_accepted / total_applications * 100) if total_applications > 0 else 0
                        st.metric("Acceptance Rate", f"{acceptance_rate:.1f}%")
                    with col3:
                        rejection_rate = (total_rejected / total_applications * 100) if total_applications > 0 else 0
                        st.metric("Rejection Rate", f"{rejection_rate:.1f}%")
                    with col4:
                        st.metric("Pending Review", sum(pos.get('pending', 0) for pos in analytics))
                    
                    # Display per-position metrics
                    st.write("### Position-wise Metrics")
                    for pos in analytics:
                        with st.expander(pos['title']):
                            st.write(f"**Total Applications:** {pos.get('total_applications', 0)}")
                            st.write(f"**Accepted:** {pos.get('accepted', 0)}")
                            st.write(f"**Rejected:** {pos.get('rejected', 0)}")
                            st.write(f"**Pending:** {pos.get('pending', 0)}")
                else:
                    st.error("Failed to load analytics")
        except Exception as e:
            st.error(f"Error loading analytics: {str(e)}")

def main():
    SideBarLinks(show_home=True)
    show_application_review()

if __name__ == "__main__":
    main()