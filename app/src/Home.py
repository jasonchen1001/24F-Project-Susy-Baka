##################################################
# Main entry-point file for Student Career System
##################################################
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")
st.title('Student Career Management System')
st.write('\n\n')
st.write('### Welcome! Please select your role to continue:')

# Student Role (Alice Johnson)
if st.button("Login as Alice Johnson (Student)", 
            type='primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'Student'
    st.session_state['first_name'] = 'Alice'
    st.session_state['user_id'] = 1
    logger.info("Logging in as Student")
    st.switch_page('pages/00_Student_Home.py')

# School Admin Role (William Smith)
if st.button("Login as William Smith (School Administrator)",
            type='primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'School_Admin'
    st.session_state['first_name'] = 'William'
    st.session_state['admin_id'] = 1
    logger.info("Logging in as School Administrator")
    st.switch_page('pages/10_Admin_Home.py')

# HR Manager Role (John Anderson)
if st.button("Login as John Anderson (HR Manager)",
            type='primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'HR_Manager'
    st.session_state['first_name'] = 'John'
    st.session_state['hr_id'] = 1
    logger.info("Logging in as HR Manager")
    st.switch_page('pages/20_HR_Home.py')

# Maintenance Staff Role (Thomas Anderson)
if st.button("Login as Thomas Anderson (Maintenance Staff)",
            type='primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'Maintenance_Staff'
    st.session_state['first_name'] = 'Thomas'
    st.session_state['staff_id'] = 1
    logger.info("Logging in as Maintenance Staff")
    st.switch_page('pages/30_Maintenance_Home.py')

# Add system description
st.markdown("""
---
### About the Student Career Management System

This integrated platform helps:
* **Students** manage resumes and track internship applications
* **School Administrators** oversee academic records and approve co-op experiences
* **HR Managers** post internship opportunities and review applications
* **Maintenance Staff** ensure system reliability and data integrity

Choose your role above to access role-specific features.

""")

# Add some visual styling
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0483ee;
    color: white;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)