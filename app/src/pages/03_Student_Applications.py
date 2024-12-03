import streamlit as st
import requests
from datetime import datetime
from modules.nav import SideBarLinks

# Page title
st.title("Application Tracker")

# Return to Home button
if st.button("← Back to Home"):
    st.switch_page("pages/00_Student_Home.py")
    
# Authentication check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
    st.error("Please login as a Student to access this page.")
    st.stop()

# Example student user ID (adjust as needed)
user_id = 1  

# Tabs for different functionalities
tabs = st.tabs(["Active Applications", "Application History", "Available Positions", "Add New Application", "Delete Application"])

# **Active Applications Tab**
with tabs[0]:
    st.write("### Current Applications")
    try:
        with st.spinner("Loading active applications..."):
            response = requests.get(f"http://web-api:4000/student/{user_id}/applications/active")
            if response.status_code == 200:
                active_apps = response.json()
                if not active_apps:
                    st.info("No active applications found.")
                else:
                    for app in active_apps:
                        with st.expander(f"{app.get('position_title')} at {app.get('company_name')}"):
                            st.write(f"**Status:** {app.get('status', 'Unknown')}")
                            st.write(f"**Applied Date:** {app.get('sent_on', 'Unknown')}")
                            st.write(f"**Position Description:** {app.get('position_description', 'No description available.')}")
                            st.write(f"**Requirements:** {app.get('requirements', 'No requirements specified.')}")
            else:
                st.error("Unable to load active applications.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# **Application History Tab**
with tabs[1]:
    st.write("### Application History")
    try:
        with st.spinner("Loading application history..."):
            response = requests.get(f"http://web-api:4000/student/{user_id}/applications/history")
            if response.status_code == 200:
                application_history = response.json()
                if not application_history:
                    st.info("No application history found.")
                else:
                    for app in application_history:
                        with st.expander(f"{app.get('position_title')} at {app.get('company_name')}"):
                            st.write(f"**Status:** {app.get('status', 'Unknown')}")
                            st.write(f"**Applied Date:** {app.get('sent_on', 'Unknown Date')}")
                            st.write(f"**Position Description:** {app.get('position_description', 'No description available.')}")
                            st.write(f"**Requirements:** {app.get('requirements', 'No requirements specified.')}")
            else:
                st.error("Unable to load application history.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# **Available Positions Tab**
with tabs[2]:
    st.write("### Available Positions")
    try:
        with st.spinner("Loading available positions..."):
            response = requests.get(f"http://web-api:4000/student/{user_id}/applications/positions")
            if response.status_code == 200:
                available_positions = response.json()
                if not available_positions:
                    st.info("No available positions found.")
                else:
                    for position in available_positions:
                        with st.expander(f"{position.get('position_title')} at {position.get('company_name')}"):
                            st.write(f"**Status:** {position.get('status', 'Unknown')}")
                            st.write(f"**Posted Date:** {position.get('posted_date', 'Unknown Date')}")
                            st.write(f"**Position Description:** {position.get('position_description', 'No description available.')}")
                            st.write(f"**Requirements:** {position.get('requirements', 'No requirements specified.')}")
            else:
                st.error("Unable to load available positions.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# **Add New Application Tab**
with tabs[3]:
    st.write("### Add New Application")
    try:
        # Load available positions
        with st.spinner("Loading available positions..."):
            response = requests.get(f"http://web-api:4000/student/{user_id}/applications/positions")
            if response.status_code == 200:
                available_positions = response.json()
                if not available_positions:
                    st.info("No positions available for application.")
                else:
                    position_dict = {f"{pos['position_title']} at {pos['company_name']}": pos['position_id'] for pos in available_positions}
                    selected_position = st.selectbox("Select a Position", list(position_dict.keys()))
                    position_id = position_dict[selected_position]
                    position_details = next(pos for pos in available_positions if pos['position_id'] == position_id)

                    st.write(f"**Position Title:** {position_details.get('position_title')}")
                    st.write(f"**Company Name:** {position_details.get('company_name')}")
                    st.write(f"**Description:** {position_details.get('position_description', 'No description available.')}")
                    st.write(f"**Requirements:** {position_details.get('requirements', 'No requirements specified.')}")

                    # Input for application date
                    applied_date = st.date_input("Applied Date", datetime.now())

                    # Submit application
                    if st.button("Add Application"):
                        payload = {
                            "position_id": position_id,
                            "sent_on": applied_date.strftime("%Y-%m-%d"),
                            "status": "Pending"
                        }
                        add_response = requests.post(f"http://web-api:4000/student/{user_id}/applications", json=payload)
                        if add_response.status_code == 201:
                            st.success("Application successfully added!")
                            st.rerun()  # 添加自动刷新
                        else:
                            st.error(f"Failed to add application: {add_response.json().get('error', 'Unknown error')}")
            else:
                st.error("Unable to load available positions.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# **Delete Application Tab**
with tabs[4]:
    st.write("### Delete Application")
    try:
        # Load active applications for deletion
        with st.spinner("Loading applications..."):
            response = requests.get(f"http://web-api:4000/student/{user_id}/applications/active")
            if response.status_code == 200:
                active_apps = response.json()
                if not active_apps:
                    st.info("No active applications to delete.")
                else:
                    application_dict = {f"{app['position_title']} at {app['company_name']}": app['application_id'] for app in active_apps}
                    selected_application = st.selectbox("Select an Application to Delete", list(application_dict.keys()))
                    application_id = application_dict[selected_application]

                    # Delete application
                    if st.button("Delete Application"):
                        delete_response = requests.delete(f"http://web-api:4000/student/{user_id}/applications/{application_id}")
                        if delete_response.status_code == 200:
                            st.success("Application successfully deleted!")
                            st.rerun()  
                        else:
                            st.error(f"Failed to delete application: {delete_response.json().get('error', 'Unknown error')}")
            else:
                st.error("Unable to load applications.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")