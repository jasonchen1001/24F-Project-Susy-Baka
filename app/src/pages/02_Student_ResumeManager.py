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

user_id = 1  # 固定用户1

# 创建选项卡
tabs = st.tabs(["Current Resume", "Update Resume", "Resume Suggestions"])

# Current Resume Tab
with tabs[0]:
    response = requests.get(f"http://localhost:5000/api/student/{user_id}/resume/latest")
    if response.status_code == 200:
        resume = response.json()
        
        st.write("### Current Resume")
        st.write("Last Updated:", resume['time_uploaded'])
        
        # 显示简历内容
        st.write("#### Education")
        st.write(resume['education'])
        
        st.write("#### Skills")
        st.write(resume['skills'])
        
        st.write("#### Projects")
        st.write(resume['projects'])
        
        st.write("#### Co-op Experience")
        st.write(resume['co_op'])
        
        if st.button("Download Resume"):
            # 这里可以添加下载功能
            st.download_button(
                label="Download as PDF",
                data=str(resume),
                file_name=f"resume_{user_id}.pdf",
                mime="application/pdf"
            )

# Update Resume Tab
with tabs[1]:
    st.write("### Update Resume")
    
    # 获取当前简历信息作为默认值
    response = requests.get(f"http://localhost:4000/api/student/{user_id}/resume/latest")
    if response.status_code == 200:
        current_resume = response.json()
        
        education = st.text_area("Education", value=current_resume['education'])
        skills = st.text_area("Skills", value=current_resume['skills'])
        projects = st.text_area("Projects", value=current_resume['projects'])
        co_op = st.text_area("Co-op Experience", value=current_resume['co_op'])
        
        if st.button("Update Resume"):
            update_data = {
                "education": education,
                "skills": skills,
                "projects": projects,
                "co_op": co_op
            }
            
            response = requests.put(
                f"http://localhost:4000/api/student/{user_id}/resume",
                json=update_data
            )
            
            if response.status_code == 200:
                st.success("Resume updated successfully!")
            else:
                st.error("Failed to update resume")

# Resume Suggestions Tab
with tabs[2]:
    st.write("### Resume Improvement Suggestions")
    
    response = requests.get(f"http://localhost:5000/api/student/{user_id}/resume/suggestions")
    if response.status_code == 200:
        suggestions = response.json()
        
        for suggestion in suggestions:
            with st.expander(f"Suggestion {suggestion['suggestion_id']}"):
                st.write(suggestion['suggestion_text'])
                st.write(f"Created: {suggestion['time_created']}")