import streamlit as st
import requests

# Ensure the user is authenticated and has the Student role
if st.session_state.get('authenticated', False) and st.session_state.get('role') == 'Student':
    st.title("View Notifications")

    # Fetch Notifications
    if st.button("Refresh Notifications"):
        response = requests.get("http://localhost:5000/student/notifications")
        if response.status_code == 200:
            notifications = response.json()
            if notifications:
                for notification in notifications:
                    st.write(f"- **{notification['date']}**: {notification['message']}")
            else:
                st.info("No new notifications.")
        else:
            st.error("Failed to fetch notifications.")

else:
    st.error("You are not authorized to view this page.")
