# frontend/layouts/settings_layout.py
import streamlit as st

class SettingsPage:
    @staticmethod
    def render():
        st.markdown('<h2 class="section-header">Settings</h2>', unsafe_allow_html=True)
    
        col1, col2 = st.columns(2)
    
        with col1:
            st.markdown("### ACCOUNT")
            st.text_input("COMPANY NAME", value="", placeholder="Enter company name")
            st.text_input("EMAIL", value="", placeholder="Enter email")
            st.selectbox("TIMEZONE", ["UTC", "EST", "PST", "CST"])
        
        with col2:
            st.markdown("### API CONFIGURATION")
            st.text_input("API KEY", value="****-****-****", type="password")
            if st.button("REGENERATE KEY", use_container_width=True):
                st.success("NEW KEY GENERATED")
            
            st.markdown("### PREFERENCES")
            st.checkbox("AUTO-EXPORT REPORTS", value=True)
            st.checkbox("EMAIL NOTIFICATIONS", value=False)