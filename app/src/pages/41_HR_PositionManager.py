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

    st.title("Internship Position Management")

    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    # Create tabs
    tabs = st.tabs(["Manage Positions", "Post New Position", "Position Analytics"])

    # Tab 1: Manage Positions
    with tabs[0]:
        try:
            response = requests.get("http://web-api:4000/hr/internships")
            if response.status_code == 200:
                positions = response.json()
                for pos in positions:
                    with st.container():
                        st.write(f"### {pos['title']} ({pos['status']})")
                        st.write("**Description:**")
                        st.write(pos['description'])
                        st.write("**Requirements:**")
                        st.write(pos['requirements'])
                        st.write(f"**Posted on:** {pos['posted_date']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Edit", key=f"edit_{pos['position_id']}"):
                                st.session_state['editing_position'] = pos
                                st.rerun()
                        with col2:
                            if st.button("Delete", key=f"delete_{pos['position_id']}"):
                                if st.button("Confirm Delete", key=f"confirm_{pos['position_id']}"):
                                    response = requests.delete(
                                        f"http://web-api:4000/hr/internships/{pos['position_id']}"
                                    )
                                    if response.status_code == 200:
                                        st.success("Position deleted!")
                                        st.rerun()
            else:
                st.error("Failed to load positions")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Tab 2: Post New Position
    with tabs[1]:
        if 'editing_position' in st.session_state:
            st.subheader("Edit Position")
            pos = st.session_state['editing_position']
        else:
            st.subheader("Post New Position")
            pos = {}
        
        with st.form("position_form"):
            title = st.text_input("Position Title", value=pos.get('title', ''))
            description = st.text_area("Description", value=pos.get('description', ''))
            requirements = st.text_area("Requirements", value=pos.get('requirements', ''))
            status = st.selectbox("Status", ["Active", "Inactive"], 
                                index=0 if pos.get('status') == 'Active' else 1)
            
            if st.form_submit_button("Submit"):
                data = {
                    "hr_id": st.session_state['hr_id'],
                    "title": title,
                    "description": description,
                    "requirements": requirements,
                    "status": status
                }
                
                if 'editing_position' in st.session_state:
                    response = requests.put(
                        f"http://web-api:4000/hr/internships/{pos['position_id']}",
                        json=data
                    )
                    msg = "updated" if response.status_code == 200 else "update failed"
                else:
                    response = requests.post(
                        "http://web-api:4000/hr/internships",
                        json=data
                    )
                    msg = "created" if response.status_code == 201 else "creation failed"
                
                if response.status_code in [200, 201]:
                    st.success(f"Position {msg}!")
                    if 'editing_position' in st.session_state:
                        del st.session_state['editing_position']
                    st.rerun()
                else:
                    st.error(f"Position {msg}!")

    # Tab 3: Analytics
    with tabs[2]:
        try:
            response = requests.get("http://web-api:4000/hr/analytics/positions")
            if response.status_code == 200:
                analytics = response.json()
                st.write("### Overall Metrics")
                
                # Calculate totals
                total_apps = sum(int(pos.get('total_applications', 0)) for pos in analytics)
                total_accepted = sum(int(pos.get('accepted', 0)) for pos in analytics)
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Positions", len(analytics))
                with col2:
                    st.metric("Total Applications", total_apps)
                with col3:
                    rate = (total_accepted / total_apps * 100) if total_apps > 0 else 0
                    st.metric("Overall Acceptance Rate", f"{rate:.1f}%")
                
                # Position-wise metrics
                st.write("### Position Details")
                for pos in analytics:
                    st.write(f"#### {pos['title']}")
                    st.metric("Applications", int(pos.get('total_applications', 0)))
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