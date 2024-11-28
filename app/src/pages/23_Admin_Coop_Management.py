import streamlit as st
import requests

st.title("Manage Co-op Experiences")

# View co-op experiences (similar route as reports if exists)
if st.button("View Co-op Reports"):
    response = requests.get("http://localhost:5000/admin/reports")
    if response.status_code == 200:
        co_op_reports = response.json()
        if co_op_reports:
            st.table(co_op_reports)
        else:
            st.warning("No co-op reports found.")
    else:
        st.error("Failed to fetch co-op reports.")