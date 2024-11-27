import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    This is a demo app for CS 3200 Course Project.  

    The goal of this demo is to provide information on the tech stack 
    being used as well as demo some of the features of the various platforms. 

    Stay tuned for more information and features to come!
    """
        )