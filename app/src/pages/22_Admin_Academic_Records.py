import streamlit as st
import requests

st.title("Manage Academic Records")

# View Academic Records
if st.button("View Academic Records"):
    response = requests.get("http://localhost:5000/admin/records")
    if response.status_code == 200:
        records = response.json()
        st.table(records)
    else:
        st.error("Failed to fetch academic records.")

# Add Academic Record
st.subheader("Add Academic Record")
student_id = st.number_input("Student ID", min_value=1, step=1)
course = st.text_input("Course Name")
grade = st.text_input("Grade")

if st.button("Add Academic Record"):
    record_data = {"student_id": student_id, "course": course, "grade": grade}
    response = requests.post("http://localhost:5000/admin/records", json=record_data)
    if response.status_code == 201:
        st.success("Academic record added successfully!")
    else:
        st.error("Failed to add academic record.")

# Update Academic Record
st.subheader("Update Academic Record")
record_id = st.number_input("Record ID to Update", min_value=1, step=1)
new_grade = st.text_input("New Grade")

if st.button("Update Academic Record"):
    update_data = {"grade": new_grade}
    response = requests.put(f"http://localhost:5000/admin/records/{record_id}", json=update_data)
    if response.status_code == 200:
        st.success("Academic record updated successfully!")
    else:
        st.error("Failed to update academic record or record not found.")
