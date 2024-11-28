import streamlit as st
from modules.nav import SideBarLinks
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.switch_page('Home.py')

# Display sidebar navigation
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}!")
st.write("### Student Dashboard")

# Display Quick Stats
col1, col2, col3 = st.columns(3)

try:
    # Get resume count
    response = requests.get(f'http://web-api:4000/resumes')
    resumes = response.json()
    col1.metric("Total Resumes", len(resumes))

    # Get application count
    response = requests.get(f'http://web-api:4000/applications')
    applications = response.json()
    col2.metric("Total Applications", len(applications))

    # Get notification count
    response = requests.get(f'http://web-api:4000/notifications')
    notifications = response.json()
    col3.metric("New Notifications", len(notifications))

except Exception as e:
    st.error(f"Error fetching dashboard data: {str(e)}")

st.markdown("""
### Quick Actions
- Manage your resumes and applications
- View application status
- Check notifications and suggestions
""")