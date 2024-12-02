import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# API URL
API_URL = "http://web-api:4000/school_admin/students"


# Page Title
st.title("Student Information and Grade Distribution")

# Fetch Student Data
response = requests.get(API_URL)
if response.status_code == 200:
    students = response.json()
    df = pd.DataFrame(students)

    if not df.empty:
        # Display the student data table
        st.write("### Students Data")
        st.dataframe(df)

        # Process and display grade distribution
        if "grade" in df.columns:
            try:
                # Ensure grades are numeric for plotting
                df["grade"] = pd.to_numeric(df["grade"], errors="coerce")
                grade_counts = df["grade"].dropna().value_counts().sort_index()

                # Plot grade distribution
                st.write("### Grade Distribution")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(grade_counts.index, grade_counts.values, color='skyblue')
                ax.set_xlabel("Grade")
                ax.set_ylabel("Count")
                ax.set_title("Grade Distribution")
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error processing grade distribution: {e}")
        else:
            st.warning("Grade data is not available in the dataset.")
    else:
        st.info("No student data found.")
else:
    st.error(f"Failed to fetch student data from the API. Status Code: {response.status_code}")
