import streamlit as st
import pandas as pd
import requests

# Page Title
st.title("Student Grades Management")

# Input for Student ID
user_id = st.text_input("Enter Student ID to Query Grades:")

if user_id:
    # Fetch grades for the given student ID
    try:
        response = requests.get(f"http://web-api:4000/school_admin/students/{user_id}/grades")
        if response.status_code == 200:
            grades = response.json()
            if grades:
                # Display academic records in a table
                st.write("### Academic Records")
                df = pd.DataFrame(grades)
                st.dataframe(df)

                # Input for Grade ID to edit
                grade_id = st.text_input("Enter Grade ID to Edit:")
                if grade_id:
                    course_name = st.text_input("New Course Name:")
                    grade = st.number_input("New Grade (0.0 - 4.0):", min_value=0.0, max_value=4.0, step=0.1)
                    if st.button("Update Grade"):
                        update_data = {"course_name": course_name, "grade": grade}
                        update_response = requests.put(
                            f"http://web-api:4000/school_admin/students/{user_id}/grades/{grade_id}",
                            json=update_data
                        )
                        if update_response.status_code == 200:
                            st.success("Grade updated successfully!")
                        else:
                            st.error(f"Failed to update grade. Error: {update_response.json().get('error', 'Unknown error')}")
            else:
                st.info("No grades found for this student.")
        else:
            st.error(f"Failed to fetch grades from the API. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    # **Add Grade Section**
    st.write("### Add a New Grade")
    course_name = st.text_input("Course Name:")
    grade = st.number_input("Grade (0.0 - 4.0):", min_value=0.0, max_value=4.0, step=0.1)
    recorded_by = st.text_input("Recorded By (e.g., Instructor Name):")
    if st.button("Add Grade"):
        try:
            add_data = {"course_name": course_name, "grade": grade, "recorded_by": recorded_by}
            add_response = requests.post(f"http://web-api:4000/school_admin/students/{user_id}/grades", json=add_data)
            if add_response.status_code == 201:
                st.success("Grade added successfully!")
            else:
                st.error(f"Failed to add grade. Error: {add_response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # **Delete Grade Section**
    st.write("### Delete a Grade")
    grade_id = st.text_input("Enter Grade ID to Delete:")
    if grade_id and st.button("Delete Grade"):
        try:
            delete_response = requests.delete(f"http://web-api:4000/school_admin/students/{user_id}/grades/{grade_id}")
            if delete_response.status_code == 200:
                st.success("Grade deleted successfully!")
            else:
                st.error(f"Failed to delete grade. Error: {delete_response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
