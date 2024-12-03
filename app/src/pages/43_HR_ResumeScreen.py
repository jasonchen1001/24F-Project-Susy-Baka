import streamlit as st
import requests
from modules.nav import SideBarLinks
import logging
import time

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("Resume Screening System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    # Create tabs
    tabs = st.tabs(["Review Resumes", "Screening History", "Analytics"])

    # Tab 1: Review Resumes
    with tabs[0]:
        try:
            response = requests.get("http://web-api:4000/hr/resumes")
            if response.status_code == 200:
                resumes = response.json()
                
                if not resumes:
                    st.info("No resumes to review.")
                else:
                    for resume in resumes:
                        with st.container():
                            st.write(f"### {resume['full_name']} - {resume['doc_name']}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Student:** {resume['full_name']}")
                                st.write(f"**Email:** {resume['email']}")
                                st.write(f"**Uploaded:** {resume['time_uploaded']}")
                            
                            with col2:
                                if resume.get('education'):
                                    st.write("**Education:**")
                                    st.info(resume['education'])
                                if resume.get('skills'):
                                    st.write("**Skills:**")
                                    st.info(resume['skills'])
                            
                            if resume.get('projects') or resume.get('co_op'):
                                with st.expander("View Experience"):
                                    if resume.get('projects'):
                                        st.write("**Projects:**")
                                        st.info(resume['projects'])
                                    if resume.get('co_op'):
                                        st.write("**Co-op Experience:**")
                                        st.info(resume['co_op'])
                            
                            if resume.get('latest_suggestion'):
                                st.write("**Previous Feedback:**")
                                st.info(resume['latest_suggestion'])
                            
                            with st.form(f"feedback_form_{resume['resume_id']}"):
                                feedback = st.text_area("Enter Feedback")
                                if st.form_submit_button("Submit Feedback"):
                                    if not feedback:
                                        st.warning("Please enter feedback before submitting.")
                                    else:
                                        try:
                                            response = requests.post(
                                                f"http://web-api:4000/hr/resumes/{resume['resume_id']}/suggestions",
                                                json={"suggestion_text": feedback}
                                            )
                                            
                                            if response.status_code == 201:
                                                st.success("Feedback submitted successfully!")
                                                st.rerun()
                                            else:
                                                st.error(f"Failed to submit feedback. Status code: {response.status_code}")
                                                st.error(f"Error details: {response.text}")
                                        except Exception as e:
                                            st.error(f"Error submitting feedback: {str(e)}")
                            
                            st.divider()
            else:
                st.error("Failed to load resumes")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Tab 2: Screening History
    with tabs[1]:
        try:
            response = requests.get("http://web-api:4000/hr/resumes")
            if response.status_code == 200:
                resumes = response.json()
                resumes_with_feedback = [r for r in resumes if r.get('latest_suggestion')]
                
                if resumes_with_feedback:
                    st.write(f"### Found {len(resumes_with_feedback)} reviewed resumes")
                    for resume in resumes_with_feedback:
                        with st.container():
                            st.write(f"### {resume['full_name']} - {resume['doc_name']}")
                            st.write(f"**Last Updated:** {resume['time_uploaded']}")
                            st.write("**Feedback:**")
                            st.info(resume['latest_suggestion'])
                            st.divider()
                else:
                    st.info("No feedback history available.")
            else:
                st.error("Failed to load screening history")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Tab 3: Analytics
    with tabs[2]:
        try:
            response = requests.get("http://web-api:4000/hr/resumes")
            if response.status_code == 200:
                resumes = response.json()
                
                # Calculate analytics
                total_resumes = len(resumes)
                resumes_with_feedback = sum(1 for r in resumes if r.get('latest_suggestion'))
                
                # Display metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Resumes", total_resumes)
                with col2:
                    st.metric("Reviewed Resumes", resumes_with_feedback)
                
                # Display resume statistics
                st.write("### Resume Statistics")
                if resumes:
                    resume_data = {
                        "Student": [r['full_name'] for r in resumes],
                        "Upload Date": [r['time_uploaded'] for r in resumes],
                        "Has Feedback": ['Yes' if r.get('latest_suggestion') else 'No' for r in resumes]
                    }
                    st.dataframe(resume_data, use_container_width=True)
                else:
                    st.info("No data available for statistics.")
            else:
                st.error("Failed to load analytics")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    SideBarLinks(show_home=True)
    main()