import streamlit as st
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks
import logging
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_performance_data():
    try:
        response = requests.get('http://localhost:5000/api/system/performance')
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            st.error("Failed to load performance data")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading performance data: {str(e)}")
        st.error("Error connecting to server")
        return pd.DataFrame()

def show_performance_monitor():
    st.title('System Performance Monitor')
    
    # Check authentication
    if not st.session_state.get('authenticated') or st.session_state.get('role') != 'Maintenance_Staff':
        st.error('Please login as Maintenance Staff to access this page')
        st.stop()
    
    # Load performance data
    df = load_performance_data()
    if df.empty:
        return
    
    # Create performance metrics visualization
    st.write("### Performance Trends")
    fig = px.line(df, x='last_update', y='metrics', 
                  color='database_name', 
                  title='System Performance Metrics')
    st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed metrics table
    st.write("### Detailed Metrics")
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        selected_db = st.multiselect('Filter by Database:', 
                                   options=df['database_name'].unique(),
                                   default=[])
    with col2:
        severity_filter = st.multiselect('Filter by Severity:', 
                                       options=df['severity'].unique(),
                                       default=[])
    
    # Apply filters
    filtered_df = df.copy()
    if selected_db:
        filtered_df = filtered_df[filtered_df['database_name'].isin(selected_db)]
    if severity_filter:
        filtered_df = filtered_df[filtered_df['severity'].isin(severity_filter)]
    
    # Display filtered data
    st.dataframe(filtered_df, use_container_width=True)
    
    # Add update monitoring form
    st.write("### Update Monitoring Parameters")
    with st.form("update_monitoring"):
        selected_database = st.selectbox('Select Database:', 
                                       options=df['database_name'].unique())
        metrics = st.text_input('Metrics:')
        alerts = st.text_input('Alerts:')
        severity = st.selectbox('Severity:', ['Low', 'Medium', 'High'])
        
        if st.form_submit_button("Update"):
            try:
                database_id = df[df['database_name'] == selected_database]['database_id'].iloc[0]
                response = requests.put(
                    'http://localhost:5000/api/system/performance',
                    json={
                        'database_id': database_id,
                        'metrics': metrics,
                        'alerts': alerts,
                        'severity': severity
                    }
                )
                if response.status_code == 200:
                    st.success("Monitoring parameters updated successfully")
                else:
                    st.error("Failed to update monitoring parameters")
            except Exception as e:
                logger.error(f"Error updating monitoring parameters: {str(e)}")
                st.error("Error connecting to server")

def main():
    SideBarLinks(show_home=True)
    show_performance_monitor()

if __name__ == "__main__":
    main()