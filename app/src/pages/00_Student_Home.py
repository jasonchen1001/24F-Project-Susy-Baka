import streamlit as st
# Page Title
st.title("Student Dashboard")

# Description
st.write("Welcome, Alice Johnson! Below are your tools for managing your account.")

# Navigation Buttons
if st.button("Manage Resumes"):
    st.session_state["page"] = "01_Resume_Management"
    st.rerun()

if st.button("Manage Applications"):
    st.session_state["page"] = "02_Application_Management"
    st.rerun()

if st.button("View Notifications"):
    st.session_state["page"] = "03_Notifications"
    st.rerun()