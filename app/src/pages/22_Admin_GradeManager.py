import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("Student Grades Management")

# Return to Home button
if st.button("← Back to Home"):
    st.switch_page("pages/20_Admin_Home.py")
    
user_id = st.text_input("Enter Student ID to Query Grades:")

if user_id:
    response = requests.get(f"http://web-api:4000/school_admin/students/{user_id}/grades")
    if response.status_code == 200:
        grades = response.json()
        df = pd.DataFrame(grades)
        st.write("### Academic Records")
        st.dataframe(df)

        grade_id = st.text_input("Enter Grade ID to Edit:")
        if grade_id:
            course_name = st.text_input("New Course Name:")
            grade = st.number_input("New Grade (0.0 - 4.0):", min_value=0.0, max_value=4.0)
            if st.button("Update Grade"):
                update_data = {"course_name": course_name, "grade": grade}
                update_response = requests.put(f"http://web-api:4000/school_admin/students/{user_id}/grades/{grade_id}", json=update_data)
                if update_response.status_code == 200:
                    st.success("Grade updated successfully!")
                else:
                    st.error("Failed to update grade.")
    else:
        st.error("Failed to fetch grades from the API.")
