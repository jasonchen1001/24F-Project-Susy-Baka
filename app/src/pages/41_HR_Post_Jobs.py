import streamlit as st
import requests

# Ensure the user is authenticated and has the HR_Manager role
if st.session_state.get('authenticated', False) and st.session_state.get('role') == 'HR_Manager':
    st.title("Post Jobs")

    # View Job Listings
    if st.button("View Job Listings"):
        response = requests.get("http://localhost:5000/hr/jobs")
        if response.status_code == 200:
            jobs = response.json()
            st.table(jobs)
        else:
            st.error("Failed to fetch job listings.")

    # Post New Job
    st.subheader("Post a New Job")
    job_title = st.text_input("Job Title")
    job_description = st.text_area("Job Description")
    job_salary = st.number_input("Salary", min_value=0, step=1000)

    if st.button("Post Job"):
        job_data = {"title": job_title, "description": job_description, "salary": job_salary}
        response = requests.post("http://localhost:5000/hr/jobs", json=job_data)
        if response.status_code == 201:
            st.success("Job posted successfully!")
        else:
            st.error("Failed to post job.")
else:
    st.error("You are not authorized to view this page.")
