import requests
import streamlit as st

def generate_btn(product_name, product_description, brand_values, target_mood, campaign_tone, API_URL):
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("GENERATE", type="primary", use_container_width=True, key="generate_main"):
            if not product_name or not product_description:
                st.error("MISSING REQUIRED FIELDS")
            else:
                st.session_state.loading = True

                request_data = {
                    "product_name": product_name,
                    "product_description": product_description,
                    "brand_values": [v.lower() for v in brand_values],
                    "target_mood": [m.lower() for m in target_mood],
                    "campaign_tone": campaign_tone.lower()
                }

                with st.spinner("ANALYZING..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/api/generate-targeting",
                            json=request_data,
                            timeout=60
                        )

                        if response.status_code == 200:
                            st.session_state.generated_data = response.json()
                            st.session_state.loading = False
                            st.success("GENERATION COMPLETE")
                            st.session_state.current_page = 'analyze'
                            st.rerun()
                        else:
                            st.error(f"ERROR: {response.status_code}")

                    except Exception as e:
                        st.error(f"CONNECTION FAILED: {e}")
                        st.session_state.loading = False
