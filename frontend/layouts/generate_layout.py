import streamlit as st
from builders.form_builder import FormBuilder
from components.buttons import generate_btn

API_URL = st.secrets["API_URL"] 

class GeneratePage:
    @staticmethod
    def render():
        st.markdown('<h2 class="section-header">Product Configuration</h2>', unsafe_allow_html=True)

        # Render the form
        FormBuilder.render_product_form()
        st.markdown('<div class="grid-line"></div>', unsafe_allow_html=True)

        # Extract values from session state
        product_name = st.session_state.get("product_name_input", "")
        product_description = st.session_state.get("product_desc_input", "")
        brand_values = st.session_state.get("brand_values_input", [])
        target_mood = st.session_state.get("target_mood_input", [])
        campaign_tone = st.session_state.get("tone_slider", "BALANCED")

        # Show generate button
        generate_btn(product_name, product_description, brand_values, target_mood, campaign_tone, API_URL)
