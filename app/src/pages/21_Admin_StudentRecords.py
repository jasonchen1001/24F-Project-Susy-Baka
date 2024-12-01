import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

# Page config
st.title("Student Records Management")

# Authentication Check
if not st.session_state.get("authenticated") or st.session_state.get("role") != "School_Admin":
    st.error("Please login as a School Administrator to access this page.")
    st.stop()

# Tabs for different functionalities
tabs = st.tabs(["View Students", "Add New Student", "Student Statistics"])

# View Students Tab
with tabs[0]:
    st.write("### Search Student Records")
    search_query = st.text_input("Search by Name or ID (Optional)")
    params = {}
    
    if search_query:
        if search_query.isdigit():
            params["id"] = search_query
        else:
            params["name"] = search_query

    with st.spinner("Loading student records..."):
        try:
            response = requests.get("http://web-api:4000/students", params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"Error loading student records: {e}")
            response = None

    if response and response.status_code == 200:
        students = pd.DataFrame(response.json())
        if students.empty:
            st.info("No matching records found.")
        else:
            st.write("### Student Records")
            st.dataframe(students, hide_index=True)
    else:
        st.error("Failed to load student records.")

# Add New Student Tab
with tabs[1]:
    st.write("### Add a New Student")
    with st.form("add_student_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        dob = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        submitted = st.form_submit_button("Add Student")
        if submitted:
            with st.spinner("Adding student..."):
                try:
                    response = requests.post(
                        "http://web-api:4000/students",
                        json={
                            "full_name": full_name,
                            "email": email,
                            "dob": dob.isoformat(),
                            "gender": gender
                        }
                    )
                    response.raise_for_status()
                    if response.status_code == 201:
                        st.success("Student added successfully!")
                    else:
                        st.error(f"Failed to add student. {response.json().get('error', 'Unknown error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error adding student: {e}")

# Student Statistics Tab
with tabs[2]:
    st.write("### Student Statistics")
    with st.spinner("Loading statistics..."):
        try:
            response = requests.get("http://web-api:4000/reports")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"Error loading student statistics: {e}")
            response = None

    if response and response.status_code == 200:
        stats = response.json()[0]  # Assuming response contains a list with one stats record
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Students", stats.get("total_students", "N/A"))
        col2.metric("Total Co-ops", stats.get("total_coops", "N/A"))
        col3.metric("Average GPA", round(stats.get("avg_grade", 0), 2))
    else:
        st.error("Failed to load student statistics.")

# Main function to include sidebar links
def main():
    SideBarLinks(show_home=True)

if __name__ == "__main__":
    main()
