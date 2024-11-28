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
            response = requests.get("http://localhost:4000/hr/resumes")
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
                        
                        with col2:
                            # Add feedback form within the expander
                            with st.form(f"feedback_form_{resume['resume_id']}"):
                                feedback = st.text_area("Enter Feedback")
                                if st.form_submit_button("Submit Feedback"):
                                    response = requests.post(
                                        f"http://localhost:4000/hr/resumes/{resume['resume_id']}/suggestions",
                                        json={"suggestion_text": feedback}
                                    )
                                    if response.status_code == 201:
                                        st.success("Feedback submitted successfully!")
                                        st.rerun()
                                        
        except Exception as e:
            st.error(f"Error loading resumes: {str(e)}")
    
    # Tab 2: Screening History
    with tab2:
        try:
            response = requests.get("http://localhost:4000/hr/resumes")
            if response.status_code == 200:
                resumes = response.json()
                
                # Create a more detailed view of screening history
                for resume in resumes:
                    if resume.get('latest_suggestion'):
                        with st.expander(f"{resume['full_name']} - {resume['doc_name']}"):
                            st.write(f"**Student:** {resume['full_name']}")
                            st.write(f"**Resume Version:** {resume['doc_name']}")
                            st.write(f"**Last Updated:** {resume['time_uploaded']}")
                            st.write("**Feedback:**")
                            st.info(resume['latest_suggestion'])
                            
        except Exception as e:
            st.error(f"Error loading screening history: {str(e)}")
    
    # Tab 3: Analytics
    with tab3:
        try:
            response = requests.get("http://localhost:4000/hr/resumes")
            if response.status_code == 200:
                resumes = response.json()
                
                # Calculate some basic analytics
                total_resumes = len(resumes)
                resumes_with_feedback = sum(1 for r in resumes if r.get('latest_suggestion'))
                
                # Display metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Resumes", total_resumes)
                with col2:
                    st.metric("Resumes with Feedback", resumes_with_feedback)
                    
                # Display resume statistics
                st.write("### Resume Activity")
                if resumes:
                    resume_data = {
                        "Student": [r['full_name'] for r in resumes],
                        "Upload Date": [r['time_uploaded'] for r in resumes],
                        "Has Feedback": ['Yes' if r.get('latest_suggestion') else 'No' for r in resumes]
                    }
                    st.dataframe(resume_data)
                
        except Exception as e:
            st.error(f"Error loading analytics: {str(e)}")

def main():
    SideBarLinks(show_home=True)
    show_resume_screen()

if __name__ == "__main__":
    main()
