# frontend/layouts/settings_layout.py
import streamlit as st
import pandas as pd
import plotly.express as px

class SettingsPage:
    @staticmethod
    def render():
        st.markdown("## SETTINGS")
        
        tab1, tab2, tab3, tab4 = st.tabs(["ACCOUNT", "TEAM", "INTEGRATIONS", "BILLING"])
        
        with tab1:
            st.markdown("### ACCOUNT SETTINGS")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Company Name", value="company_name")
                st.text_input("Primary Email", value="marketing@company.com")
                st.selectbox("Industry", ["Technology", "Retail", "Healthcare", "Finance", "Other"])
            
            with col2:
                st.selectbox("Company Size", ["1-10", "11-50", "51-200", "201-500", "500+"])
                st.selectbox("Time Zone", ["UTC", "EST", "CST", "PST"])
                st.selectbox("Language", ["English", "Spanish", "French", "German"])
            
            if st.button("SAVE CHANGES", type="primary"):
                st.success("Settings saved successfully!")
        
        with tab2:
            st.markdown("### TEAM MANAGEMENT")
            
            # Team members table
            team_data = {
                'Name': ['John Smith', 'Sarah Johnson', 'Mike Chen'],
                'Email': ['john@company.com', 'sarah@company.com', 'mike@company.com'],
                'Role': ['Admin', 'Editor', 'Viewer'],
                'Last Active': ['Today', 'Yesterday', '3 days ago']
            }
            team_df = pd.DataFrame(team_data)
            st.dataframe(team_df, use_container_width=True, hide_index=True)
            
            # Add team member
            with st.expander("ADD TEAM MEMBER"):
                new_email = st.text_input("Email Address")
                new_role = st.selectbox("Role", ["Admin", "Editor", "Viewer"])
                if st.button("SEND INVITATION"):
                    st.success("Invitation sent!")
        
        with tab3:
            st.markdown("### CONNECTED INTEGRATIONS")
            
            integrations = [
                {"name": "HubSpot", "status": "Connected", "last_sync": "2 hours ago"},
                {"name": "Google Analytics", "status": "Connected", "last_sync": "1 hour ago"},
                {"name": "Salesforce", "status": "Not Connected", "last_sync": "-"},
                {"name": "Meta Business", "status": "Connected", "last_sync": "3 hours ago"}
            ]
            
            for integration in integrations:
                col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
                
                with col1:
                    st.markdown(f"**{integration['name']}**")
                with col2:
                    if integration['status'] == "Connected":
                        st.success(integration['status'])
                    else:
                        st.warning(integration['status'])
                with col3:
                    st.text(f"Last sync: {integration['last_sync']}")
                with col4:
                    if integration['status'] == "Connected":
                        st.button("DISCONNECT", key=f"disc_{integration['name']}")
                    else:
                        st.button("CONNECT", key=f"conn_{integration['name']}")
        
        with tab4:
            st.markdown("### BILLING & USAGE")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Plan", "Professional", "")
            with col2:
                st.metric("Monthly Usage", "847 / 1000", "API Calls")
            with col3:
                st.metric("Next Billing", "July 1, 2024", "$299/month")
            
            st.markdown("### USAGE HISTORY")
            
            # Usage chart
            usage_data = pd.DataFrame({
                'Month': ['January', 'February', 'March', 'April', 'May', 'June'],
                'API Calls': [650, 720, 810, 890, 920, 847]
            })
            
            fig = px.line(usage_data, x='Month', y='API Calls', 
                        title="Monthly API Usage",
                        markers=True)
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif"),
                showlegend=False
            )
            fig.update_traces(line_color='#000000')
            st.plotly_chart(fig, use_container_width=True)