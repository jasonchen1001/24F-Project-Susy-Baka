import streamlit as st
from modules.nav import SideBarLinks
import logging

# Configure Logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Page Title
st.title("HR Management System")

# Description
st.write("Welcome to the HR Management Dashboard!")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
    st.error("Please login as HR Manager to access this page.")
    st.stop()

# Welcome Message
st.write(f"Welcome, {st.session_state.get('first_name')}!")
st.write("\n")

# Create layout with columns
col1, col2 = st.columns(2)

with col1:
    if st.button("Manage Internship Positions", use_container_width=True):
        st.switch_page("pages/41_HR_PositionManager.py")
            
    if st.button("Review Applications", use_container_width=True):
        st.switch_page("pages/42_HR_ApplicationReview.py")
            
    if st.button("Resume Screening", use_container_width=True):
        st.switch_page("pages/43_HR_ResumeScreen.py")

with col2:
    st.write("### Recruitment Overview")
    st.metric("Active Positions", "12")
    st.metric("Pending Applications", "25")
    st.metric("Resumes to Review", "15")