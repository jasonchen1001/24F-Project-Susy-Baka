import streamlit as st
import requests

st.title("Manage Academic Records")

# View all academic records
if st.button("View Academic Records"):
    with st.spinner("Fetching academic records..."):
        response = requests.get("http://localhost:5000/admin/academic-records")
        if response.status_code == 200:
            records = response.json()
            if records:
                st.table(records)
            else:
                st.warning("No academic records found.")
        else:
            st.error("Failed to fetch academic records.")

# Add a new academic record
st.subheader("Add New Academic Record")
student_id = st.text_input("Student ID")
course_name = st.text_input("Course Name")
grade = st.text_input("Grade")
if st.button("Add Academic Record"):
    record_data = {"student_id": student_id, "course_name": course_name, "grade": grade, "recorded_by": 1}
    response = requests.post("http://localhost:5000/admin/academic-records", json=record_data)
    if response.status_code == 201:
        st.success("Academic record added successfully!")
    else:
        st.error("Failed to add academic record.")