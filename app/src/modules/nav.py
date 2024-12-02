import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def AboutPageNav():
    st.sidebar.page_link("pages/70_About.py", label="About", icon="ℹ️")

#### ------------------------ Student Role ------------------------
def StudentHomeNav():
    st.sidebar.page_link("pages/00_Student_Home.py", label="Student Dashboard", icon="👨‍🎓")

def PersonalInfoNav():
    st.sidebar.page_link("pages/01_Student_PersonalInfo.py", label="Personal Information", icon="👤")

def ResumeManagementNav():
    st.sidebar.page_link("pages/02_Student_ResumeManager.py", label="Resume Management", icon="📄")

def ApplicationManagementNav():
    st.sidebar.page_link("pages/03_Student_Applications.py", label="Application Tracker", icon="📝")

#### ------------------------ School Admin Role ------------------------
def AdminHomeNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="Admin Dashboard", icon="👨‍💼")

def StudentRecordsNav():
    st.sidebar.page_link("pages/21_Admin_StudentRecords.py", label="Student Records", icon="📚")

# 管理员首页导航
def AdminHomeNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="Admin Dashboard", icon="👨‍💼")

# 学生记录管理导航
def StudentRecordsNav():
    st.sidebar.page_link("pages/21_Admin_StudentRecords.py", label="Student Records", icon="📚")

# 成绩管理导航
def GradeManagerNav():
    st.sidebar.page_link("pages/22_Admin_GradeManager.py", label="Grade Management", icon="📝")

# 实习审核导航
def CoopApprovalNav():
    st.sidebar.page_link("pages/23_Admin_CoopApproval.py", label="Co-op Approvals", icon="✅")

#### ------------------------ HR Role ------------------------
def HRHomeNav():
    st.sidebar.page_link("pages/40_HR_Home.py", label="HR Dashboard", icon="👥")

def InternshipNav():
    st.sidebar.page_link("pages/41_HR_PositionManager.py", label="Manage Internships", icon="💼")

def ApplicationReviewNav():
    st.sidebar.page_link("pages/42_HR_ApplicationReview.py", label="Review Applications", icon="📋")

def ResumeScreenNav():
    st.sidebar.page_link("pages/43_HR_ResumeScreen.py", label="Resume Screening", icon="📄")

        #### ------------------------ Maintenance Role ------------------------
def MaintenanceHomeNav():
    st.sidebar.page_link("pages/60_Maintenance_Home.py", label="System Dashboard", icon="🔧")

def AlertMonitorNav():
    st.sidebar.page_link("pages/61_Alert_Monitor.py", label="Monitor Alerts", icon="🔔")


def AlterationManagerNav():
    st.sidebar.page_link("pages/64_Alteration_Manager.py", label="Data Alterations", icon="📝")

def DatabaseManagerNav():
    st.sidebar.page_link("pages/65_Database_Manager.py", label="Database Management", icon="🗃️")

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
            PersonalInfoNav()
            ResumeManagementNav()
            ApplicationManagementNav()
        elif st.session_state["role"] == "School_Admin":
            AdminHomeNav()
            StudentRecordsNav()
        elif st.session_state["role"] == "HR_Manager":
            HRHomeNav()
            InternshipNav()
            ApplicationReviewNav()
            ResumeScreenNav()
        elif st.session_state["role"] == "Maintenance_Staff":
            MaintenanceHomeNav()
            AlertMonitorNav()
            AlterationManagerNav()
            DatabaseManagerNav()
    
    AboutPageNav()

    # Ensure session state keys are initialized
    if "role" not in st.session_state:
        st.session_state["role"] = None
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False





    # Logout button
    if st.sidebar.button("Logout"):
        # Reset session state 
        st.session_state["role"] = None
        st.session_state["authenticated"] = False



