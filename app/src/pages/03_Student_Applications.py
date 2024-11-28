import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page config
st.title("Application Tracker")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
    st.error("Please login as a Student to access this page.")
    st.stop()

user_id = 1  # 固定用户1

# 创建选项卡
tabs = st.tabs(["Active Applications", "Application History", "Available Positions"])

# Active Applications Tab
with tabs[0]:
    st.write("### Current Applications")
    
    response = requests.get(f"http://localhost:4000/api/student/{user_id}/applications/active")
    if response.status_code == 200:
        active_apps = response.json()
        
        for app in active_apps:
            with st.expander(f"{app['position_title']} at {app['company_name']}"):
                st.write(f"**Status:** {app['status']}")
                st.write(f"**Applied:** {app['sent_on']}")
                st.write(f"**Position Description:** {app['description']}")
                st.write(f"**Requirements:** {app['requirements']}")

# Application History Tab
with tabs[1]:
    st.write("### Application History")
    
    response = requests.get(f"http://localhost:4000/api/student/{user_id}/applications/all")
    if response.status_code == 200:
        all_apps = response.json()
        
        # 创建数据框展示
        df = pd.DataFrame(all_apps)
        
        # 状态筛选器
        status_filter = st.multiselect(
            "Filter by Status",
            options=['Pending', 'Accepted', 'Rejected'],
            default=['Pending', 'Accepted', 'Rejected']
        )
        
        filtered_df = df[df['status'].isin(status_filter)]
        st.dataframe(filtered_df, use_container_width=True)
        
        # 统计图表
        st.write("### Application Statistics")
        status_counts = df['status'].value_counts()
        st.bar_chart(status_counts)

# Available Positions Tab
with tabs[2]:
    st.write("### Available Internship Positions")
    
    response = requests.get("http://localhost:4000/api/internships/active")
    if response.status_code == 200:
        positions = response.json()
        
        for position in positions:
            with st.expander(f"{position['title']} - {position['hr_name']}"):
                st.write(f"**Description:** {position['description']}")
                st.write(f"**Requirements:** {position['requirements']}")
                st.write(f"**Posted Date:** {position['posted_date']}")
                
                # 检查是否已申请
                check_response = requests.get(
                    f"http://localhost:4000/api/student/{user_id}/application/check/{position['position_id']}"
                )
                
                if check_response.status_code == 200:
                    if not check_response.json()['applied']:
                        if st.button("Apply Now", key=position['position_id']):
                            apply_response = requests.post(
                                f"http://localhost:4000/api/student/{user_id}/application/submit",
                                json={"position_id": position['position_id']}
                            )
                            if apply_response.status_code == 200:
                                st.success("Application submitted successfully!")
                            else:
                                st.error("Failed to submit application")
                    else:
                        st.info("Already applied to this position")