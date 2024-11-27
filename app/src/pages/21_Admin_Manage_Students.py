import streamlit as st
import requests

st.title("Manage Students")

# View All Students
if st.button("View All Students"):
    response = requests.get("http://localhost:5000/admin/students")
    if response.status_code == 200:
        students = response.json()
        st.table(students)
    else:
        st.error("Failed to fetch student data.")

# Add New Student
st.subheader("Add New Student")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
major = st.text_input("Major")
gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, step=0.1)

if st.button("Add Student"):
    student_data = {"name": name, "email": email, "major": major, "gpa": gpa}
    response = requests.post("http://localhost:5000/admin/students", json=student_data)
    if response.status_code == 201:
        st.success("Student added successfully!")
    else:
        st.error("Failed to add student.")

# Remove Student
st.subheader("Remove Student")
student_id = st.number_input("Enter Student ID to Remove", min_value=1, step=1)

if st.button("Remove Student"):
    response = requests.delete(f"http://localhost:5000/admin/students/{student_id}")
    if response.status_code == 200:
        st.success("Student removed successfully!")
    else:
        st.error("Failed to remove student or student not found.")
