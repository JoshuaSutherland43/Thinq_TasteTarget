# frontend/layouts/fallback_layout.py
import streamlit as st

class FallbackPage:
    @staticmethod
    def render():
        st.markdown('<h2 class="section-header">No Data Available</h2>', unsafe_allow_html=True)
        st.info("Generate a campaign first to access this section.")
        if st.button("GO TO GENERATOR", use_container_width=True):
            st.session_state.current_page = "generate"
            st.rerun()