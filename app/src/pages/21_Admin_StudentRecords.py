import streamlit as st
import pandas as pd
import requests

BASE_API_URL = "http://web-api:4000"

# Page Title
st.title("Student Grades Management")

# Return to Home button
if st.button("← Back to Home"):
    st.switch_page("pages/20_Admin_Home.py")

# Input for Student ID
user_id = st.text_input("Enter Student ID to Query Grades:")

if user_id:
    # Fetch grades
    response = requests.get(f"{BASE_API_URL}/school_admin/students/{user_id}/grades")
    
    if response.status_code == 200:
        grades = response.json()
        df = pd.DataFrame(grades)
        df = df[['grade_id', 'course_name', 'grade', 'recorded_date']]
        st.write("### Academic Records")
        st.dataframe(df, hide_index=True)  
        
        # Display current grades for reference
        if not df.empty and 'grade_id' in df.columns:
            st.write("Available Grade IDs:")
            for _, row in df.iterrows():
                st.write(f"Grade ID: {row['grade_id']} - Course: {row['course_name']} - Grade: {row['grade']}")
        
        # Edit Grade Section
        st.write("### Edit Grade")
        edit_grade_id = st.text_input("Enter Grade ID to Edit:", key="edit_grade_id")
        if edit_grade_id:
            try:
                grade_id_int = int(edit_grade_id) 
                new_course_name = st.text_input("New Course Name:", key="edit_course_name")
                new_grade = st.number_input(
                    "New Grade (0.0 - 4.0):", 
                    min_value=0.0, 
                    max_value=4.0,
                    key="edit_grade_value"
                )
                
                if st.button("Update Grade", key="update_button"):
                    update_data = {
                        "course_name": new_course_name,
                        "grade": float(new_grade)
                    }
                    update_url = f"{BASE_API_URL}/school_admin/students/{user_id}/grades/{grade_id_int}"
                    st.write(f"Debug - Update URL: {update_url}")
                    st.write(f"Debug - Update Data: {update_data}")
                    
                    update_response = requests.put(
                        update_url,
                        json=update_data
                    )
                    st.write(f"Debug - Response Status: {update_response.status_code}")
                    st.write(f"Debug - Response Content: {update_response.text}")
                    
                    if update_response.status_code == 200:
                        st.success("Grade updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to update grade. Status Code: {update_response.status_code}")
                        st.error(f"Error message: {update_response.text}")
            except ValueError:
                st.error("Please enter a valid numeric Grade ID")
        
        # Add Grade Section
        st.write("### Add a New Grade")
        new_course_name = st.text_input("Course Name:", key="add_course_name")
        new_grade = st.number_input(
            "Grade (0.0 - 4.0):",
            min_value=0.0,
            max_value=4.0,
            step=0.1,
            key="add_grade_value"
        )
        recorded_by = st.text_input("Recorded By (e.g., Instructor Name):")
        
        if st.button("Add Grade", key="add_button"):
            add_data = {
                "course_name": new_course_name,
                "grade": float(new_grade),
                "recorded_by": recorded_by
            }
            add_response = requests.post(
                f"{BASE_API_URL}/school_admin/students/{user_id}/grades",
                json=add_data
            )
            if add_response.status_code == 201:
                st.success("Grade added successfully!")
                st.rerun()
            else:
                st.error(f"Failed to add grade. Status Code: {add_response.status_code}")
                st.error(f"Error message: {add_response.text}")
        
        # Delete Grade Section
        st.write("### Delete a Grade")
        delete_grade_id = st.text_input("Enter Grade ID to Delete:", key="delete_grade_id")
        
        if delete_grade_id:
            try:
                grade_id_int = int(delete_grade_id)  
                if st.button("Delete Grade", key="delete_button"):

                    delete_url = f"{BASE_API_URL}/school_admin/students/{user_id}/grades/{grade_id_int}"
                    st.write(f"Debug - Delete URL: {delete_url}")
                    
                    delete_response = requests.delete(delete_url)
                    st.write(f"Debug - Response Status: {delete_response.status_code}")
                    st.write(f"Debug - Response Content: {delete_response.text}")
                    
                    if delete_response.status_code == 200:
                        st.success("Grade deleted successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to delete grade. Status Code: {delete_response.status_code}")
                        st.error(f"Error message: {delete_response.text}")
            except ValueError:
                st.error("Please enter a valid numeric Grade ID")
    else:
        st.error(f"Failed to fetch grades. Status Code: {response.status_code}")
        st.error(f"Error message: {response.text}")