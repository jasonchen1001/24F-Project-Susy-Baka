import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def create_position_form():
    """Create form for adding/editing positions"""
    with st.form("position_form"):
        title = st.text_input("Position Title")
        description = st.text_area("Description")
        requirements = st.text_area("Requirements")
        status = st.selectbox("Status", ["Active", "Inactive"])
        
        submitted = st.form_submit_button("Submit Position")
        if submitted and title and description and requirements:
            return {
                "hr_id": st.session_state['hr_id'],
                "title": title,
                "description": description,
                "requirements": requirements,
                "status": status
            }
    return None

def show_position_manager():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("Internship Position Management")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    st.divider()
    
    # Main operations
    tab1, tab2, tab3 = st.tabs(["Manage Positions", "Post New Position", "Position Analytics"])
    
    # Tab 1: Manage Positions
    with tab1:
        try:
            response = requests.get("http://localhost:4000/hr/internships")
            if response.status_code == 200:
                positions = response.json()
                for pos in positions:
                    with st.expander(f"{pos['title']} ({pos['status']})"):
                        st.write("#### Description")
                        st.write(pos['description'])
                        st.write("#### Requirements")
                        st.write(pos['requirements'])
                        st.write(f"Posted on: {pos['posted_date']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Edit", key=f"edit_{pos['position_id']}"):
                                st.session_state['editing_position'] = pos
                                st.rerun()
                        with col2:
                            if st.button("Delete", key=f"delete_{pos['position_id']}", type="secondary"):
                                if st.button("Confirm Delete", key=f"confirm_{pos['position_id']}", type="primary"):
                                    response = requests.delete(f"http://localhost:4000/hr/internships/{pos['position_id']}")
                                    if response.status_code == 200:
                                        st.success("Position deleted successfully!")
                                        st.rerun()
        except Exception as e:
            st.error(f"Error loading positions: {str(e)}")

    # Tab 2: Post New Position
    with tab2:
        if 'editing_position' in st.session_state:
            st.subheader("Edit Position")
            position_data = create_position_form()
            if position_data:
                try:
                    response = requests.put(
                        f"http://localhost:4000/hr/internships/{st.session_state['editing_position']['position_id']}",
                        json=position_data
                    )
                    if response.status_code == 200:
                        st.success("Position updated successfully!")
                        del st.session_state['editing_position']
                        st.rerun()
                except Exception as e:
                    st.error(f"Error updating position: {str(e)}")
        else:
            st.subheader("Post New Position")
            position_data = create_position_form()
            if position_data:
                try:
                    response = requests.post(
                        "http://localhost:4000/hr/internships",
                        json=position_data
                    )
                    if response.status_code == 201:
                        st.success("Position created successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error creating position: {str(e)}")

    # Tab 3: Analytics
    with tab3:
        try:
            response = requests.get("http://localhost:4000/hr/analytics/positions")
            if response.status_code == 200:
                analytics = response.json()
                st.write("### Position Analytics")
                for pos in analytics:
                    st.write(f"#### {pos['title']}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Applications", pos['total_applications'])
                    with col2:
                        st.metric("Accepted", pos['accepted'])
                    with col3:
                        st.metric("Pending", pos['pending'])
        except Exception as e:
            st.error(f"Error loading analytics: {str(e)}")

def main():
    SideBarLinks(show_home=True)
    show_position_manager()

if __name__ == "__main__":
    main()
