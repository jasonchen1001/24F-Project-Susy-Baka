import streamlit as st
from modules.nav import SideBarLinks
import logging

# Configure Logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Page Title
st.title("Student Career Management")

# Description
st.write("Welcome to your Career Management Dashboard!")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
    st.error("Please login as a Student to access this page.")
    st.stop()

# Welcome Message
st.write(f"Welcome, {st.session_state.get('first_name')}!")
st.write("\n")

# Create layout with columns
col1, col2 = st.columns(2)

with col1:
    if st.button("Manage Resumes", use_container_width=True):
        st.switch_page("pages/01_Student_ResumeManager.py")
            
    if st.button("Track Applications", use_container_width=True):
        st.switch_page("pages/02_Student_ApplicationTracker.py")
            
    if st.button("View Co-op Records", use_container_width=True):
        st.switch_page("pages/03_Student_CoopRecords.py")

with col2:
    st.write("### Your Overview")
    st.metric("Active Applications", "5")
    st.metric("Resume Versions", "2")
    st.metric("Latest Co-op", "TechCorp (2023)")