import streamlit as st

# Page Title
st.title("School Administrator Dashboard")

# Description
st.write("Welcome, William Smith! Below are your tools for managing the system.")

# Navigation Buttons
if st.button("Manage Students"):
    st.session_state["page"] = "21_Admin_Manage_Students"
    st.experimental_rerun()

if st.button("Manage Academic Records"):
    st.session_state["page"] = "22_Admin_Academic_Records"
    st.experimental_rerun()

if st.button("Manage Co-op Experiences"):
    st.session_state["page"] = "23_Admin_Coop_Management"
    st.experimental_rerun()
