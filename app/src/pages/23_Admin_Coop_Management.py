import streamlit as st
import requests

st.title("Manage Co-op Experiences")

# View Co-op Records
if st.button("View Co-op Records"):
    response = requests.get("http://localhost:5000/admin/coops")
    if response.status_code == 200:
        coops = response.json()
        st.table(coops)
    else:
        st.error("Failed to fetch co-op records.")

# Approve Co-op Experience
st.subheader("Approve Co-op Experience")
coop_id = st.number_input("Enter Co-op ID to Approve", min_value=1, step=1)

if st.button("Approve Co-op"):
    response = requests.put(f"http://localhost:5000/admin/coops/{coop_id}/approve")
    if response.status_code == 200:
        st.success("Co-op experience approved successfully!")
    else:
        st.error("Failed to approve co-op experience or record not found.")

# Remove Co-op Experience
st.subheader("Remove Co-op Experience")
remove_coop_id = st.number_input("Enter Co-op ID to Remove", min_value=1, step=1)

if st.button("Remove Co-op"):
    response = requests.delete(f"http://localhost:5000/admin/coops/{remove_coop_id}")
    if response.status_code == 200:
        st.success("Co-op experience removed successfully!")
    else:
        st.error("Failed to remove co-op experience or record not found.")
