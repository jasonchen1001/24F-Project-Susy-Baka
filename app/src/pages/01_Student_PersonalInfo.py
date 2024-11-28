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
            with st.spinner("Loading personal information..."):
                response = requests.get(f"http://web-api:4000/student/info/1")
                if response.status_code == 200:
                    student_info = response.json()

                     # 页面显示内容
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("### Personal Details")
                        st.write(f"**Name:** {student_info.get('full_name', 'N/A')}")
                        st.write(f"**Email:** {student_info.get('email', 'N/A')}")
                        st.write(f"**Date of Birth:** {student_info.get('dob', 'N/A')}")
                        st.write(f"**Gender:** {student_info.get('gender', 'N/A')}")
                    with col2:
                        st.write("### Additional Information")
                        st.write(f"**Education:** {student_info.get('education', 'N/A')}")
                        st.write(f"**Skills:** {student_info.get('skills', 'N/A')}")
                        st.write(f"**Projects:** {student_info.get('projects', 'N/A')}")
                        st.write(f"**Co-op:** {student_info.get('co_op', 'N/A')}")
                else:
                    st.error("Failed to load student information")


        # Academic Records Tab 同理
        with tabs[1]:
            with st.spinner("Loading academic records..."):
                response = requests.get(f"http://web-api:4000/student/{user_id}/grades")
                if response.status_code == 200:
                    grades = response.json()
                    
                    st.write("### Academic Performance")
                    for grade in grades:
                        st.metric(
                            label=grade.get('course_name', 'Unknown Course'),
                            value=f"GPA: {grade.get('grade', 'N/A')}"
                        )

        # Co-op History Tab 同理
        with tabs[2]:
            with st.spinner("Loading co-op history..."):
                response = requests.get(f"http://web-api:4000/student/{user_id}/coops")
                if response.status_code == 200:
                    coops = response.json()
                    
                    if not coops:
                        st.info("No co-op history found.")
                    else:
                    # 显示 Co-op 数据
                        st.write("### Co-op Experience")
                        for coop in coops:
                            with st.expander(f"{coop.get('company_name', 'Unknown Company')} - {coop.get('start_date', 'N/A')} to {coop.get('end_date', 'N/A')}"):
                                st.write(f"**Company:** {coop.get('company_name', 'N/A')}")
                                st.write(f"**Period:** {coop.get('start_date', 'N/A')} - {coop.get('end_date', 'N/A')}")
                                st.write(f"**Approved By:** {coop.get('approved_by', 'N/A')}")
                else:
                    t.error(f"Failed to load co-op history. Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error loading  {str(e)}")
        st.error(f"An error occurred while loading the  {e}")

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()