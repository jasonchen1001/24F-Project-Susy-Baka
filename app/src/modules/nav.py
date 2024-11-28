import streamlit as st
#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def AboutPageNav():
    st.sidebar.page_link("pages/70_About.py", label="About", icon="ℹ️")

#### ------------------------ Student Role ------------------------
def StudentHomeNav():
    st.sidebar.page_link("pages/00_Student_Home.py", label="Student Dashboard", icon="👨‍🎓")

def ResumeManagementNav():
    st.sidebar.page_link("pages/01_Resume_Management.py", label="Resume Management", icon="📄")

def ApplicationManagementNav():
    st.sidebar.page_link("pages/02_Application_Management.py", label="Applications", icon="📝")

def NotificationsNav():
    st.sidebar.page_link("pages/03_Notifications.py", label="Notifications", icon="🔔")

#### ------------------------ School Admin Role ------------------------
def AdminHomeNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="Admin Dashboard", icon="👨‍💼")

def StudentRecordsNav():
    st.sidebar.page_link("pages/21_Student_Records.py", label="Student Records", icon="📚")

#### ------------------------ HR Role ------------------------
def HRHomeNav():
    st.sidebar.page_link("pages/40_HR_Home.py", label="HR Dashboard", icon="👥")

def InternshipNav():
    st.sidebar.page_link("pages/41_Internships.py", label="Manage Internships", icon="💼")

#### ------------------------ Maintenance Role ------------------------
def MaintenanceHomeNav():
    st.sidebar.page_link("pages/60_Maintenance_Home.py", label="System Dashboard", icon="🔧")

def SystemMonitoringNav():
    st.sidebar.page_link("pages/61_System_Monitoring.py", label="Monitoring", icon="📊")

def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar based on user's role
    """
    # Add logo to sidebar
    st.sidebar.image("assets/logo.png", width=150)

    # If no logged in user, redirect to Home
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        HomeNav()

    # Show role-specific navigation
    if st.session_state["authenticated"]:
        if st.session_state["role"] == "Student":
            StudentHomeNav()
            ResumeManagementNav()
            ApplicationManagementNav()
            NotificationsNav()

        elif st.session_state["role"] == "School_Admin":
            AdminHomeNav()
            StudentRecordsNav()

        elif st.session_state["role"] == "HR_Manager":
            HRHomeNav()
            InternshipNav()

        elif st.session_state["role"] == "Maintenance_Staff":
            MaintenanceHomeNav()
            SystemMonitoringNav()

        # Always show About page
        AboutPageNav()

        # Logout button
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")