import streamlit as st
import requests

# Ensure the user is authenticated and has the Student role
if st.session_state.get('authenticated', False) and st.session_state.get('role') == 'Student':
    st.title("Manage Applications")

    # View Application Listings
    if st.button("View Applications"):
        response = requests.get("http://localhost:5000/student/applications")
        if response.status_code == 200:
            applications = response.json()
            if applications:
                st.table(applications)
            else:
                st.info("No applications found.")
        else:
            st.error("Failed to fetch applications.")

    # Add New Application
    st.subheader("Add a New Application")
    company_name = st.text_input("Company Name")
    position_title = st.text_input("Position Title")
    application_status = st.selectbox("Status", ["Pending", "Interview", "Offered", "Rejected"])

    if st.button("Add Application"):
        application_data = {
            "company": company_name,
            "position": position_title,
            "status": application_status
        }
        response = requests.post("http://localhost:5000/student/applications", json=application_data)
        if response.status_code == 201:
            st.success("Application added successfully!")
        else:
            st.error("Failed to add application.")

else:
    st.error("You are not authorized to view this page.")
