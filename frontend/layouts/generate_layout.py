import streamlit as st
from builders.form_builder import FormBuilder
from components.buttons import generate_btn
from builders.current_form import current_form

API_URL = st.secrets["API_URL"] 

class GeneratePage:
    @staticmethod
    def render():
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

