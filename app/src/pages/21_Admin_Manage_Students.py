import streamlit as st
import requests
##11
st.title("Manage Students")

# Fetch all students
if st.button("View All Students"):
    with st.spinner("Fetching students..."):
        response = requests.get("http://localhost:5000/admin/students")
        if response.status_code == 200:
            students = response.json()
            if students:
                st.table(students)
            else:
                st.warning("No students found.")
        else:
            st.error("Failed to fetch students.")

# Add a new student
st.subheader("Add New Student")
full_name = st.text_input("Full Name")
email = st.text_input("Email")
dob = st.date_input("Date of Birth")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
if st.button("Add Student"):
    student_data = {"full_name": full_name, "email": email, "dob": str(dob), "gender": gender}
    response = requests.post("http://localhost:5000/admin/students", json=student_data)
    if response.status_code == 201:
        st.success("Student added successfully!")
    else:
        st.error("Failed to add student.")

# Update student details
st.subheader("Update Student Details")
student_id = st.text_input("Student ID to Update")
if st.button("Update Student"):
    updated_data = {"full_name": full_name, "email": email, "dob": str(dob), "gender": gender}
    response = requests.put(f"http://localhost:5000/admin/students/{student_id}", json=updated_data)
    if response.status_code == 200:
        st.success("Student updated successfully!")
    else:
        st.error("Failed to update student.")

# Delete student
st.subheader("Delete Student")
delete_student_id = st.text_input("Student ID to Delete")
if st.button("Delete Student"):
    response = requests.delete(f"http://localhost:5000/admin/students/{delete_student_id}")
    if response.status_code == 200:
        st.success("Student deleted successfully!")
    else:
        st.error("Failed to delete student.")
import streamlit as st
import requests

st.title("Manage Students")

# Fetch all students
if st