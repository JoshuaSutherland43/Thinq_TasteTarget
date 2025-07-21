import streamlit as st

def current_form():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### PRODUCT INFORMATION")
            product_name = st.text_input(
                "PRODUCT/CAMPAIGN NAME *",
                placeholder="e.g., Summer Collection 2024",
                help="Enter a memorable name for your product or campaign"
            )
            
            product_description = st.text_area(
                "DESCRIPTION *",
                placeholder="Describe your product, its features, benefits, and what makes it unique...",
                height=150,
                help="The more detail you provide, the better the AI can understand your product"
            )
            
            industry = st.selectbox(
                "INDUSTRY",
                ["Fashion & Retail", "Technology", "Food & Beverage", "Beauty & Wellness",
                 "Travel & Hospitality", "Financial Services", "Healthcare", "Education", "Other"]
            )
        
        with col2:
            st.markdown("### BRAND & AUDIENCE")
            brand_values = st.multiselect(
                "BRAND VALUES *",
                ["Sustainability", "Innovation", "Quality", "Authenticity", 
                 "Luxury", "Accessibility", "Creativity", "Trust", 
                 "Performance", "Community", "Heritage", "Simplicity"],
                help="Select up to 5 core values that represent your brand"
            )
            
            target_mood = st.multiselect(
                "TARGET AUDIENCE MINDSET *",
                ["Aspirational", "Practical", "Adventurous", "Sophisticated", 
                 "Eco-conscious", "Tech-savvy", "Traditional", "Trendy",
                 "Budget-conscious", "Premium-seeking", "Health-focused", "Social"],
                help="Select the mindsets that best describe your target audience"
            )
            
            campaign_tone = st.select_slider(
                "CAMPAIGN TONE",
                options=["Professional", "Friendly", "Playful", "Bold", "Inspirational"],
                value="Friendly",
                help="Choose the overall tone for your marketing messages"
            )
        
        # Advanced Options
        with st.expander("ADVANCED OPTIONS"):
            col1, col2 = st.columns(2)
            with col1:
                include_competitors = st.checkbox("Include competitor analysis", value=False)
                generate_visuals = st.checkbox("Generate visual guidelines", value=True)
            with col2:
                num_personas = st.slider("Number of personas", 2, 5, 3)
                languages = st.multiselect("Additional languages", ["Spanish", "French", "German", "Japanese"])
        