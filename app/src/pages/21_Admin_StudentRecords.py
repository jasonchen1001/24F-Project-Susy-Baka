import streamlit as st
import pandas as pd
import requests

# Page Title
st.title("Student Grades Management")

# Input for Student ID
user_id = st.text_input("Enter Student ID to Query Grades:")

if user_id:
    # Fetch grades
    response = requests.get(f"http://web-api:4000/school_admin/students/{user_id}/grades")
    if response.status_code == 200:
        grades = response.json()
        df = pd.DataFrame(grades)
        st.write("### Academic Records")
        st.dataframe(df)

        # **Update Grade Section**
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
        st.error(f"Failed to fetch grades from the API. Status Code: {response.status_code}")

    # **Add Grade Section**
    st.write("### Add a New Grade")
    course_name = st.text_input("Course Name:")
    grade = st.number_input("Grade (0.0 - 4.0):", min_value=0.0, max_value=4.0, step=0.1)
    recorded_by = st.text_input("Recorded By (e.g., Instructor Name):")
    if st.button("Add Grade"):
        add_data = {"course_name": course_name, "grade": grade, "recorded_by": recorded_by}
        add_response = requests.post(f"http://web-api:4000/school_admin/students/{user_id}/grades", json=add_data)
        if add_response.status_code == 201:
            st.success("Grade added successfully!")
        else:
            st.error(f"Failed to add grade. Status Code: {add_response.status_code}")

    # **Delete Grade Section**
    st.write("### Delete a Grade")
    grade_id = st.text_input("Enter Grade ID to Delete:")
    if grade_id and st.button("Delete Grade"):
        delete_response = requests.delete(f"http://web-api:4000/school_admin/students/{user_id}/grades/{grade_id}")
        if delete_response.status_code == 200:
            st.success("Grade deleted successfully!")
        else:
            st.error(f"Failed to delete grade. Status Code: {delete_response.status_code}")
