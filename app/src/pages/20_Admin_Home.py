import streamlit as st
from modules.nav import SideBarLinks
import logging

# Configure Logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Page Title
    st.title("School Administrator Dashboard")

    # Description
    st.write("Welcome to the Administration Management System!")

    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "School_Admin":
        st.error("Please login as School Administrator to access this page.")
        st.stop()

    # Welcome Message
    st.write(f"Welcome, {st.session_state.get('first_name', 'Admin')}!")
    st.write("\n")

    # Create layout with columns
    col1, col2 = st.columns(2)

    with col1:
        if st.button("View Student Records", use_container_width=True):
            st.switch_page("pages/21_Admin_StudentRecords.py")  
        if st.button("Review Grades", use_container_width=True):
            st.switch_page("pages/22_Admin_GradeManager.py")  
        if st.button("Review co-op", use_container_width=True):
            st.switch_page("pages/23_Admin_CoopApproval.py")  


if __name__ == "__main__":
    # Initialize session state keys
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "role" not in st.session_state:
        st.session_state["role"] = None

    # Render Sidebar
    SideBarLinks(show_home=True)

    # Run the main application
    main()
