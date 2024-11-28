import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page config
st.title("Application Tracker")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
    st.error("Please login as a Student to access this page.")
    st.stop()

user_id = 1  

tabs = st.tabs(["Active Applications", "Application History", "Available Positions"])

# Active Applications Tab
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
                        position_title = app.get('position_title', 'Unknown Position')
                        company_name = app.get('company_name', 'Unknown Company')
                        position_description = app.get('position_description', 'No description available.')
                        requirements = app.get('requirements', 'No requirements specified.')
                        status = app.get('status', 'Unknown')
                        sent_on = app.get('sent_on', 'Unknown Date')

                        with st.expander(f"{position_title} at {company_name}"):
                            st.write(f"**Status:** {status}")
                            st.write(f"**Applied Date:** {sent_on}")
                            st.write(f"**Position Description:** {position_description}")
                            st.write(f"**Requirements:** {requirements}")

            else:
                st.error("Failed to load active applications.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# Application History Tab
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
                st.error("Failed to load application history.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")



# Available Positions Tab
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
                st.error("Failed to load available positions.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
