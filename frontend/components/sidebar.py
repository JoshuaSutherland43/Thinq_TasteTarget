# frontend/components/sidebar.py
import streamlit as st

class Sidebar:
    @staticmethod
    def render():
        with st.sidebar:
            st.markdown("<div style='padding: 2rem 0;'><h2 style='color: white;'>TASTETARGET</h2></div>", unsafe_allow_html=True)
        
        st.markdown("### QUICK LINKS")
        
        if st.button("◐ DASHBOARD", use_container_width=True, key="side_dash"):
            st.session_state.current_page = 'generate'
            st.rerun()
        
        if st.button("◑ HISTORY", use_container_width=True, key="side_hist"):
            st.info("Coming soon")
        
        if st.button("◒ SUPPORT", use_container_width=True, key="side_support"):
            st.info("support@tastetarget.ai")
        
        st.markdown("---")
        
        st.markdown("""
        <div style='position: absolute; bottom: 2rem; left: 1rem; right: 1rem;'>
            <p style='color: #666666; font-size: 0.75rem; text-align: center;'>
                VERSION 1.0.0<br>
                ENTERPRISE EDITION
            </p>
        </div>
        """, unsafe_allow_html=True)
