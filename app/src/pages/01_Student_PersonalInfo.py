import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from modules.nav import SideBarLinks

# Page config
st.title("Personal Information")

# Return to Home button
if st.button("← Back to Home"):
    st.switch_page("pages/00_Student_Home.py")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "Student":
    st.error("Please login as a Student to access this page.")
    st.stop()

user_id = st.session_state.get("user_id")
tabs = st.tabs(["Basic Information", "Academic Records", "Co-op History"])

# Basic Information Tab
with tabs[0]:
    with st.spinner("Loading personal information..."):
        response = requests.get(f"http://web-api:4000/student/info/{user_id}")
        
    if response.status_code == 200:
        info = response.json()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Personal Details")
            st.write(f"**Full Name:** {info.get('full_name', 'N/A')}")
            st.write(f"**Email:** {info.get('email', 'N/A')}")
            st.write(f"**Date of Birth:** {info.get('dob', 'N/A')}")
            st.write(f"**Gender:** {info.get('gender', 'N/A')}")
        
        with col2:
            st.write("### Academic Status")
            st.write(f"**Student ID:** {info.get('user_id', 'N/A')}")
            st.write(f"**Major:** Computer Science")
            if info.get('education'):
                st.write(f"**{info.get('education', 'N/A')}**")
    else:
        st.error("Failed to load personal information")

# Academic Records Tab
with tabs[1]:
    with st.spinner("Loading academic records..."):
        response = requests.get(f"http://web-api:4000/student/{user_id}/grades")
        
    if response.status_code == 200:
        grades = response.json()
        st.write("### Academic Records")
        
        if grades:
            df = pd.DataFrame(grades)
            df['recorded_date'] = pd.to_datetime(df['recorded_date']).dt.strftime('%Y-%m-%d')
            
            df.columns = ['Course', 'Grade', 'Recorded Date', 'Recorded By']
            
            st.dataframe(df, hide_index=True)
            
        else:
            st.info("No academic records found")

# Co-op History Tab
with tabs[2]:
    with st.spinner("Loading co-op history..."):
        response = requests.get(f"http://web-api:4000/student/{user_id}/coops")
        
    if response.status_code == 200:
        coops = response.json()
        st.write("### Co-op History")
        
        if coops:
            df = pd.DataFrame(coops)

            df['start_date'] = pd.to_datetime(df['start_date'], format='mixed').dt.strftime('%Y-%m-%d')
            df['end_date'] = pd.to_datetime(df['end_date'], format='mixed').dt.strftime('%Y-%m-%d')
            
            df.columns = ['ID', 'Company', 'Start Date', 'End Date', 'Approved By']

            df = df.drop('ID', axis=1)
            st.dataframe(df, hide_index=True)
            
            st.write("### Co-op Timeline")
            for coop in coops:
                st.write(f"**{coop['company_name']}**")
                st.write(f"_{pd.to_datetime(coop['start_date'], format='mixed').strftime('%Y-%m-%d')} to {pd.to_datetime(coop['end_date'], format='mixed').strftime('%Y-%m-%d')}_")
                st.write(f"Approved by: {coop['approved_by']}")
                st.write("---")
        else:
            st.info("No co-op records found")
def main():
    SideBarLinks(show_home=True)
if __name__ == "__main__":
    main()