import streamlit as st
from builders.current_form import current_form
from components.buttons import generate_btn
from components.sidebar import Sidebar

API_URL = st.secrets["API_URL"]

class DashboardPage:
    @staticmethod
    def render():
        st.title("🎯 TasteTarget Dashboard")
        st.markdown("Use the form below to generate audience insights.")

        # Render the input form
        current_form()

        # Extract values from session state
        product_name = st.session_state.get("product_name_input", "")
        product_description = st.session_state.get("product_desc_input", "")
        brand_values = st.session_state.get("brand_values_input", [])
        target_mood = st.session_state.get("target_mood_input", [])
        campaign_tone = st.session_state.get("tone_slider", "BALANCED")

        # Render generate button with values
        generate_btn(product_name, product_description, brand_values, target_mood, campaign_tone, API_URL)

        # Optional Sidebar
        # Sidebar.render()

        # Footer
        st.markdown('</br>', unsafe_allow_html=True)
        st.markdown('<div class="grid-line" style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <p style='color: #000000; font-weight: 600; font-size: 0.875rem; letter-spacing: 0.1em;'>
                TASTETARGET © 2024
            </p>
            <p style='color: #666666; font-size: 0.75rem; margin-top: 0.5rem;'>
                AI-POWERED AUDIENCE INTELLIGENCE
            </p>
        </div>
        """, unsafe_allow_html=True)
