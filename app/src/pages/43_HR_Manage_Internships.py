import streamlit as st
import requests

st.title("Manage Internship Postings")

# View Internship Postings
if st.button("View Internship Postings"):
    response = requests.get("http://localhost:5000/hr/internships")
    if response.status_code == 200:
        internships = response.json()
        st.table(internships)
    else:
        st.error("Failed to fetch internship postings.")

# Other functionalities can be added here similar to adding, updating, and deleting internship postings.
