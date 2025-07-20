import streamlit as st

def current_form():
        col1, col2 = st.columns([1, 1], gap="large")     
        with col1:
            product_name = st.text_input(
                "PRODUCT NAME",
                placeholder="Enter product name",
                key="product_name_input"
            )
            
            product_description = st.text_area(
                "PRODUCT DESCRIPTION",
                placeholder="Describe your product in detail...",
                height=150,
                key="product_desc_input"
            )
            
            campaign_tone = st.select_slider(
                "CAMPAIGN TONE",
                options=["MINIMAL", "BALANCED", "EXPRESSIVE", "BOLD"],
                value="BALANCED",
                key="tone_slider"
            )
        
        with col2:
            brand_values = st.multiselect(
                "BRAND VALUES",
                options=["SUSTAINABILITY", "INNOVATION", "QUALITY", "AUTHENTICITY", 
                        "MINIMALISM", "LUXURY", "ACCESSIBILITY", "CRAFT", 
                        "TRANSPARENCY", "COMMUNITY"],
                key="brand_values_input"
            )
            
            target_mood = st.multiselect(
                "TARGET MOOD",
                options=["CONSCIOUS", "MODERN", "BOLD", "SOPHISTICATED", 
                        "AUTHENTIC", "MINDFUL", "CREATIVE", "PROFESSIONAL"],
                key="target_mood_input"
            )
            
            # Advanced Settings in Minimal Expander
            with st.expander("ADVANCED SETTINGS"):
                include_analytics = st.checkbox("Include Analytics", value=True)
                export_format = st.selectbox(
                    "Export Format",
                    ["PDF", "JSON", "CSV", "POWERPOINT"]
                )