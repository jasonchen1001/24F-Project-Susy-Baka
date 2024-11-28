import streamlit as st
import requests
from modules.nav import SideBarLinks
import logging

# Configure logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
        st.error("Please login as a Student to access this page.")
        st.stop()

    st.title("Personal Information")
    
    user_id = 1  # 固定用户1

    # 创建选项卡
    tabs = st.tabs(["Basic Info", "Academic Records", "Co-op History"])

    try:
        # Basic Info Tab
        with tabs[0]:
            # 添加加载动画
            with st.spinner("Loading personal information..."):
                response = requests.get(f"http://web-api:4000/student/{user_id}/info")
                if response.status_code == 200:
                    student_info = response.json()
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("### Personal Details")
                        st.write(f"**Name:** {student_info['full_name']}")
                        st.write(f"**Email:** {student_info['email']}")
                        st.write(f"**Date of Birth:** {student_info['dob']}")
                        st.write(f"**Gender:** {student_info['gender']}")

        # Academic Records Tab
        with tabs[1]:
            with st.spinner("Loading academic records..."):
                response = requests.get(f"http://web-api:4000/student/{user_id}/grades")
                if response.status_code == 200:
                    grades = response.json()
                    st.write("### Academic Performance")
                    for grade in grades:
                        st.metric(
                            label=grade['course_name'],
                            value=f"GPA: {grade['grade']}"
                        )

        # Co-op History Tab
        with tabs[2]:
            with st.spinner("Loading co-op history..."):
                response = requests.get(f"http://web-api:4000/student/{user_id}/coops")
                if response.status_code == 200:
                    coops = response.json()
                    st.write("### Co-op Experience")
                    for coop in coops:
                        with st.expander(f"{coop['company_name']} - {coop['start_date']} to {coop['end_date']}"):
                            st.write(f"**Company:** {coop['company_name']}")
                            st.write(f"**Period:** {coop['start_date']} - {coop['end_date']}")

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        st.error("An error occurred while loading the data")

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()