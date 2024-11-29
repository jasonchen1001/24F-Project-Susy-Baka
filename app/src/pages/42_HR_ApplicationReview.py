import streamlit as st
import requests
from modules.nav import SideBarLinks
import logging

# Configure logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("Application Review System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    # Create tabs
    tabs = st.tabs(["Pending Applications", "Review History", "Analytics"])

    # Tab 1: Pending Applications
    with tabs[0]:
        with st.spinner("Loading pending applications..."):
            try:
                response = requests.get("http://web-api:4000/hr/applications", params={"status": "Pending"})
                if response.status_code == 200:
                    applications = response.json()
                    positions = {}
                    
                    # Group applications by position
                    for app in applications:
                        pos_id = app.get('position_id')
                        if pos_id:
                            if pos_id not in positions:
                                positions[pos_id] = []
                            positions[pos_id].append(app)
                    
                    if positions:
                        st.write(f"### Found {len(applications)} pending applications")
                        
                        for pos_id, apps in positions.items():
                            st.write(f"### {apps[0]['position_title']}")
                            
                            for app in apps:
                                with st.container():
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.write(f"**Applicant:** {app['full_name']}")
                                        st.write(f"**Email:** {app['email']}")
                                        st.write(f"**Applied:** {app['sent_on']}")
                                    
                                    with col2:
                                        if st.button("Accept", key=f"accept_{app['application_id']}", type="primary"):
                                            response = requests.put(
                                                f"http://web-api:4000/hr/applications/{app['application_id']}",
                                                json={"status": "Accepted"}
                                            )
                                            if response.status_code == 200:
                                                st.success("Application accepted!")
                                                st.rerun()
                                        
                                        if st.button("Reject", key=f"reject_{app['application_id']}", type="secondary"):
                                            response = requests.put(
                                                f"http://web-api:4000/hr/applications/{app['application_id']}",
                                                json={"status": "Rejected"}
                                            )
                                            if response.status_code == 200:
                                                st.success("Application rejected!")
                                                st.rerun()
                                    st.divider()
                    else:
                        st.info("No pending applications to review.")
                else:
                    st.error("Failed to load applications")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Tab 2: Review History
    with tabs[1]:
        try:
            response = requests.get("http://web-api:4000/hr/applications")
            if response.status_code == 200:
                applications = response.json()
                
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "Accepted", "Rejected", "Pending"]
                )
                
                # Filter applications
                filtered_apps = applications if status_filter == "All" else [
                    app for app in applications 
                    if app.get('status', '').upper() == status_filter.upper()
                ]
                
                if filtered_apps:
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total", len(applications))
                    with col2:
                        st.metric("Accepted", sum(1 for app in applications if app.get('status') == 'Accepted'))
                    with col3:
                        st.metric("Rejected", sum(1 for app in applications if app.get('status') == 'Rejected'))
                    
                    # Display applications
                    for app in filtered_apps:
                        st.write(f"### {app['full_name']} - {app['position_title']}")
                        st.write(f"**Status:** {app.get('status', 'Unknown')}")
                        st.write(f"**Applied:** {app.get('sent_on', 'Unknown')}")
                        st.divider()
                else:
                    st.info(f"No applications found with status: {status_filter}")
            else:
                st.error("Failed to load applications")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Tab 3: Analytics
    with tabs[2]:
        try:
            response = requests.get("http://web-api:4000/hr/analytics/positions")
            if response.status_code == 200:
                analytics = response.json()
                
                # Overall metrics
                total = sum(int(pos.get('total_applications', 0)) for pos in analytics)
                accepted = sum(int(pos.get('accepted', 0)) for pos in analytics)
                rejected = sum(int(pos.get('rejected', 0)) for pos in analytics)
                
                st.write("### Overall Metrics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Applications", total)
                with col2:
                    st.metric("Accepted", accepted)
                with col3:
                    st.metric("Rejected", rejected)
                with col4:
                    st.metric("Pending", total - accepted - rejected)
                
                # Position-wise metrics
                st.write("### Position-wise Metrics")
                for pos in analytics:
                    with st.expander(pos['title']):
                        pos_total = int(pos.get('total_applications', 0))
                        if pos_total > 0:
                            st.metric("Total Applications", pos_total)
                            st.write(f"Accepted: {int(pos.get('accepted', 0))}")
                            st.write(f"Rejected: {int(pos.get('rejected', 0))}")
                            st.write(f"Pending: {int(pos.get('pending', 0))}")
            else:
                st.error("Failed to load analytics")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()