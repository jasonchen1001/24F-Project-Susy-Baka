import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page config
st.title("Resume Management")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
    st.error("Please login as a Student to access this page.")
    st.stop()

user_id = 1  

tabs = st.tabs(["Current Resume", "Update Resume", "Resume Suggestions"])

# Current Resume Tab
with tabs[0]:  # Current Resume
    with st.spinner("Loading current resume..."):
        response = requests.get(f"http://web-api:4000/student/{user_id}/resume")
        if response.status_code == 200:
            resume = response.json()

            st.write("### Current Resume")
            st.write(f"**Document Name:** {resume.get('doc_name', 'N/A')}")
            st.write(f"**Education:** {resume.get('education', 'N/A')}")
            st.write(f"**Skills:** {resume.get('skills', 'N/A')}")
            st.write(f"**Projects:** {resume.get('projects', 'N/A')}")
            st.write(f"**Co-op:** {resume.get('co_op', 'N/A')}")
        else:
            st.error("Failed to load current resume")


# Update Resume Tab
with tabs[1]:  # Update Resume Tab
    with st.spinner("Loading resume details..."):
        response = requests.get(f"http://web-api:4000/student/{user_id}/resume")
        if response.status_code == 200:
            resume = response.json()

            st.write("### Update Resume")
            
            doc_name = st.text_input(
                "Document Name",
                value=resume.get('doc_name', 'Enter your Document Name...')
            )

            education = st.text_area(
                "Education",
                value=resume.get('education', 'Enter your education details...')
            )
            skills = st.text_area(
                "Skills",
                value=resume.get('skills', 'Enter your skills...')
            )

            projects = st.text_area(
                "Projects",
                value=resume.get('projects', 'Enter your projects...')
            )

            co_op = st.text_area(
                "Co-op",
                value=resume.get('co_op', 'Enter your co-op experiences...')
            )

            if st.button("Update Resume"):
                with st.spinner("Updating resume..."):

                    update_response = requests.put(
                        f"http://web-api:4000/student/{user_id}/resume",
                        json={
                            "doc_name": doc_name, 
                            "education": education,
                            "skills": skills,
                            "projects": projects,
                            "co_op": co_op
                        }
                    )
                    if update_response.status_code == 200:
                        st.success("Resume updated successfully!")
                    else:
                        st.error("Failed to update resume")
        else:
            st.error("Failed to load resume details")



# Resume Suggestions Tab
with tabs[2]:  # Resume Suggestions
    with st.spinner("Loading resume suggestions..."):
        response = requests.get(f"http://web-api:4000/student/{user_id}/resume/suggestions")
        if response.status_code == 200:
            suggestions = response.json()

            st.write("### Resume Suggestions")
            for suggestion in suggestions:
                st.write(f"- {suggestion.get('suggestion_text', 'No suggestion text')}")
        else:
            st.error("Failed to load resume suggestions")
