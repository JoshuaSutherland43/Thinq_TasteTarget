import streamlit as st


def current_form():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### PRODUCT INFORMATION")
        product_name = st.text_input(
            "PRODUCT/CAMPAIGN NAME *",
            key="product_name_input",
            placeholder="e.g., Summer Collection 2024",
            help="Enter a memorable name for your product or campaign",
        )

        product_description = st.text_area(
            "DESCRIPTION *",
            key="product_desc_input",
            placeholder="Describe your product, its features, benefits, and what makes it unique...",
            height=150,
            help="The more detail you provide, the better the AI can understand your product",
        )

        industry = st.selectbox(
            "INDUSTRY",
            [
                "Fashion & Retail",
                "Technology",
                "Food & Beverage",
                "Beauty & Wellness",
                "Travel & Hospitality",
                "Financial Services",
                "Healthcare",
                "Education",
                "Other",
            ],
            key="industry_input",
        )

    with col2:
        st.markdown("### BRAND & AUDIENCE")
        brand_values = st.multiselect(
            "BRAND VALUES *",
            [
                "Sustainability",
                "Innovation",
                "Quality",
                "Authenticity",
                "Luxury",
                "Accessibility",
                "Creativity",
                "Trust",
                "Performance",
                "Community",
                "Heritage",
                "Simplicity",
            ],
            help="Select up to 5 core values that represent your brand",
            key="brand_values_input",
        )

        target_mood = st.multiselect(
            "TARGET AUDIENCE MINDSET *",
            [
                "Aspirational",
                "Practical",
                "Adventurous",
                "Sophisticated",
                "Eco-conscious",
                "Tech-savvy",
                "Traditional",
                "Trendy",
                "Budget-conscious",
                "Premium-seeking",
                "Health-focused",
                "Social",
            ],
            help="Select the mindsets that best describe your target audience",
            key="target_mood_input",
        )

        campaign_tone = st.select_slider(
            "CAMPAIGN TONE",
            options=["Professional", "Friendly", "Playful", "Bold", "Inspirational"],
            value="Friendly",
            help="Choose the overall tone for your marketing messages",
            key="campaign_tone_input",
        )

    # Advanced Options
    with st.expander("ADVANCED OPTIONS"):
        col1, col2 = st.columns(2)
        with col1:
            include_competitors = st.checkbox(
                "Include competitor analysis",
                value=False,
                key="include_competitors_input",
            )
            generate_visuals = st.checkbox(
                "Generate visual guidelines", value=True, key="generate_visuals_input"
            )
        with col2:
            num_personas = st.slider(
                "Number of personas", 2, 5, 3, key="num_personas_input"
            )
            languages = st.multiselect(
                "Additional languages",
                ["Spanish", "French", "German", "Japanese"],
                key="languages_input",
            )
