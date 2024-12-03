import streamlit as st
import requests
import pandas as pd
from datetime import datetime


API_BASE_URL = "http://web-api:4000/maintenance_staff"

# Return to Home button
if st.button("← Back to Home"):
    st.switch_page("pages/60_Maintenance_Home.py")
    
def fetch_alterations():
    try:
        response = requests.get(f"{API_BASE_URL}/alterations")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching alterations: {str(e)}")
        return None

def update_alteration(alteration_id, alteration_type, alteration_date):
    try:
        response = requests.put(
            f"{API_BASE_URL}/alterations/{alteration_id}",
            json={
                "alteration_type": alteration_type,
                "alteration_date": alteration_date
            }
        )
        if response.status_code == 200:
            st.success("Alteration updated successfully!")
            st.rerun()
        else:
            st.error(f"Failed to update alteration. Status Code: {response.status_code}")
            st.error(f"Error details: {response.text}")
    except Exception as e:
        st.error(f"Error updating alteration: {str(e)}")

def main():
    st.title("Data Alteration Management")
    st.write("Manage data alteration history for databases.")

    alterations = fetch_alterations()

    if alterations:
        st.subheader("Current Alterations")
        df = pd.DataFrame(alterations)
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.subheader("Edit Alteration")
        selected_alteration = st.selectbox(
            "Select Alteration to Edit",
            options=df["database_id"].tolist(),
            format_func=lambda x: f"Database: {df[df['database_id']==x]['database_name'].iloc[0]} ({x})"
        )

        if selected_alteration:
            alteration_data = df[df["database_id"] == selected_alteration].iloc[0]
            with st.form("edit_alteration_form"):
                alteration_type = st.selectbox(
                    "Alteration Type",
                    options=["Data Migration", "Schema Update", "Index Rebuild"],
                    index=["Data Migration", "Schema Update", "Index Rebuild"].index(alteration_data["alteration_type"]),
                    key="edit_type"
                )
                
                current_date = datetime.strptime(
                    alteration_data["alteration_date"], 
                    "%a, %d %b %Y %H:%M:%S GMT"
                ).strftime("%Y-%m-%d")
                
                alteration_date = st.date_input(
                    "Alteration Date",
                    value=datetime.strptime(current_date, "%Y-%m-%d"),
                    key="edit_date"
                )
                
                if st.form_submit_button("Update"):
                    update_alteration(
                        selected_alteration,
                        alteration_type,
                        alteration_date.strftime("%Y-%m-%d")
                    )
    else:
        st.info("No alterations available.")

if __name__ == "__main__":
    main()