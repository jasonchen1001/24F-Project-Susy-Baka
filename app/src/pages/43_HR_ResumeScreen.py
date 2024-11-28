import streamlit as st
from modules.nav import SideBarLinks
import logging
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def show_resume_screen():
    # Authentication Check
    if not st.session_state.get("authenticated") or st.session_state.get("role") != "HR_Manager":
        st.error("Please login as HR Manager to access this page.")
        st.stop()

    st.title("Resume Screening System")
    
    # Return to Home button
    if st.button("← Back to Home"):
        st.switch_page("pages/40_HR_Home.py")
    
    st.divider()
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Review Resumes", "Screening History", "Analytics"])
    
    # Tab 1: Review Resumes
    with tab1:
        try:
            with st.spinner("Loading resumes..."):
                response = requests.get("http://web-api:4000/hr/resumes")
                if response.status_code == 200:
                    resumes = response.json()
                    
                    if not resumes:
                        st.info("No resumes to review.")
                    
                    for resume in resumes:
                        with st.expander(f"{resume['full_name']} - {resume['doc_name']}"):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.write(f"**Student:** {resume['full_name']}")
                                st.write(f"**Email:** {resume['email']}")
                                st.write(f"**Uploaded:** {resume['time_uploaded']}")
                                if resume.get('latest_suggestion'):
                                    st.write("**Latest Feedback:**")
                                    st.info(resume['latest_suggestion'])
                                
                                # Display mock resume content
                                st.write("### Resume Content")
                                st.markdown("""
                                **Education**
                                - Bachelor of Science in Computer Science
                                - GPA: 3.8/4.0
                                
                                **Skills**
                                - Programming Languages: Python, Java, JavaScript
                                - Web Technologies: React, Node.js
                                - Databases: MySQL, MongoDB
                                
                                **Projects**
                                - Student Career System (Team Project)
                                - Personal Portfolio Website
                                """)
                            
                            with col2:
                                with st.form(f"feedback_form_{resume['resume_id']}"):
                                    feedback = st.text_area("Enter Feedback")
                                    if st.form_submit_button("Submit Feedback"):
                                        with st.spinner("Submitting feedback..."):
                                            response = requests.post(
                                                f"http://web-api:4000/hr/resumes/{resume['resume_id']}/suggestions",
                                                json={"suggestion_text": feedback}
                                            )
                                            if response.status_code == 201:
                                                st.success("Feedback submitted successfully!")
                                                st.rerun()
                else:
                    st.error("Failed to load resumes")
        except Exception as e:
            st.error(f"Error loading resumes: {str(e)}")
    
    # Tab 2: Screening History
    with tab2:
        try:
            with st.spinner("Loading screening history..."):
                response = requests.get("http://web-api:4000/hr/resumes")
                if response.status_code == 200:
                    resumes = response.json()
                    
                    # Create filters
                    st.write("### Feedback History")
                    
                    # Only show resumes with feedback
                    resumes_with_feedback = [r for r in resumes if r.get('latest_suggestion')]
                    
                    if resumes_with_feedback:
                        for resume in resumes_with_feedback:
                            with st.expander(f"{resume['full_name']} - {resume['doc_name']}"):
                                st.write(f"**Student:** {resume['full_name']}")
                                st.write(f"**Resume Version:** {resume['doc_name']}")
                                st.write(f"**Last Updated:** {resume['time_uploaded']}")
                                st.write("**Feedback:**")
                                st.info(resume['latest_suggestion'])
                    else:
                        st.info("No feedback history available.")
                else:
                    st.error("Failed to load screening history")
        except Exception as e:
            st.error(f"Error loading screening history: {str(e)}")
    
    # Tab 3: Analytics
    with tab3:
        try:
            with st.spinner("Loading analytics..."):
                response = requests.get("http://web-api:4000/hr/resumes")
                if response.status_code == 200:
                    resumes = response.json()
                    
                    # Calculate analytics
                    total_resumes = len(resumes)
                    resumes_with_feedback = sum(1 for r in resumes if r.get('latest_suggestion'))
                    feedback_rate = (resumes_with_feedback / total_resumes * 100) if total_resumes > 0 else 0
                    
                    # Display metrics
                    st.write("### Resume Screening Metrics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Resumes", total_resumes)
                    with col2:
                        st.metric("Reviewed Resumes", resumes_with_feedback)
                    with col3:
                        st.metric("Review Rate", f"{feedback_rate:.1f}%")
                    
                    # Display detailed statistics
                    st.write("### Resume Statistics")
                    if resumes:
                        resume_data = {
                            "Student": [r['full_name'] for r in resumes],
                            "Upload Date": [r['time_uploaded'] for r in resumes],
                            "Has Feedback": ['Yes' if r.get('latest_suggestion') else 'No' for r in resumes]
                        }
                        st.dataframe(resume_data, use_container_width=True)
                        
                        # Add visualization
                        st.write("### Upload Timeline")
                        st.line_chart([1] * len(resumes), use_container_width=True)
                    else:
                        st.info("No data available for statistics.")
                else:
                    st.error("Failed to load analytics")
        except Exception as e:
            st.error(f"Error loading analytics: {str(e)}")

def main():
    SideBarLinks(show_home=True)
    show_resume_screen()

if __name__ == "__main__":
    main()
