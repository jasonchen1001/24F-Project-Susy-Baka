import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    Welcome to the Student Career Management App!

    This application is designed to streamline the recruitment process for students and recruiters.

    Explore features such as tracking job applications, managing resumes, exploring internship opportunities, and viewing personalized career insights.

    Stay tuned for more updates and features to enhance your recruitment experience!
    """
        )