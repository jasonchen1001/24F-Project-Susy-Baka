import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("Student Co-op Management")

user_id = st.text_input("Enter Student ID to Query Co-ops:")

if user_id:
    response = requests.get(f"http://web-api:4000/school_admin/students/{user_id}/coops")
    if response.status_code == 200:
        coops = response.json()
        df = pd.DataFrame(coops)
        st.write("### Co-op Records")
        st.dataframe(df)

        coop_id = st.text_input("Enter Co-op ID to Edit:")
        if coop_id:
            company_name = st.text_input("New Company Name:")
            start_date = st.date_input("New Start Date:")
            end_date = st.date_input("New End Date:")
            if st.button("Update Co-op"):
                update_data = {"company_name": company_name, "start_date": str(start_date), "end_date": str(end_date)}
                update_response = requests.put(f"http://web-api:4000/school_admin/students/{user_id}/coops/{coop_id}", json=update_data)
                if update_response.status_code == 200:
                    st.success("Co-op updated successfully!")
                else:
                    st.error("Failed to update co-op.")
    else:
        st.error("Failed to fetch co-ops from the API.")
