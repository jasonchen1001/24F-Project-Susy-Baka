import streamlit as st

# Page Title
st.title("HR Manager Dashboard")

# Description
st.write("Welcome, John Anderson! Below are your tools for managing HR tasks.")

# Navigation Buttons
if st.button("Post Jobs"):
    st.session_state["page"] = "41_HR_Post_Jobs"
    st.rerun()

if st.button("Review Applications"):
    st.session_state["page"] = "42_HR_Review_Applications"
    st.rerun()

if st.button("Manage Internship Postings"):
    st.session_state["page"] = "43_HR_Manage_Internships"
    st.rerun()
