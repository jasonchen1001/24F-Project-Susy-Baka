import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from modules.nav import SideBarLinks

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
# Update Resume Tab
with tabs[1]:  # Update Resume Tab
    with st.spinner("Loading resume details..."):
        response = requests.get(f"http://web-api:4000/student/{user_id}/resume")
        
    if response.status_code == 200:
        resume = response.json()
        st.write("### Update Resume")
        
        doc_name = st.text_input(
            "Document Name",
            value=resume.get('doc_name', '')
        )
        
        st.markdown("### Education (🔒 Only Updated by School Admin)")
        st.text_area(
            "Education",
            value=resume.get('education', ''),
            disabled=True,
            key="education"
        )
        
        st.markdown("### Skills (✏️ Student Editable)")
        skills = st.text_area(
            "Skills",
            value=resume.get('skills', '')
        )
        
        st.markdown("### Projects (✏️ Student Editable)")
        projects = st.text_area(
            "Projects",
            value=resume.get('projects', '')
        )
        
        st.markdown("### Co-op Experience (🔒 Only Updated by School Admin)")
        st.text_area(
            "Co-op Experience",
            value=resume.get('co_op', ''),
            disabled=True,
            key="coop"
        )

        if st.button("Update Resume"):
            update_response = requests.put(
                f"http://web-api:4000/student/{user_id}/resume",
                json={
                    "doc_name": doc_name,
                    "skills": skills,
                    "projects": projects
                }
            )
            
            if update_response.status_code == 200:
                st.success("✅ Resume updated successfully!")
                time.sleep(1)  
                st.experimental_rerun()  
            elif update_response.status_code == 403:
                st.error("❌ Education and Co-op fields can only be updated by School Admin")
            else:
                st.error("❌ Failed to update resume")
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
def main():
    SideBarLinks(show_home=True)
if __name__ == "__main__":
    main()