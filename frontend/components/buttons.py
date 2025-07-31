import requests
import streamlit as st
import time


def generate_btn(
    product_name, product_description, brand_values, target_mood, campaign_tone, API_URL
):
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button(
            "Generate Audience Intelligence",
            type="primary",
            use_container_width=True,
            key="generate_main",
        ):
            if not product_name or not product_description:
                st.error("MISSING REQUIRED FIELDS")
            else:
                st.session_state.loading = True

                with st.spinner(
                    "AI is analyzing your product and generating insights..."
                ):

                    # Progress bar
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)

                    # API Call
                    request_data = {
                        "product_name": product_name,
                        "product_description": product_description,
                        "brand_values": [v.lower() for v in brand_values],
                        "target_mood": [m.lower() for m in target_mood],
                        "campaign_tone": campaign_tone.lower(),
                    }

                    try:
                        response = requests.post(
                            f"{API_URL}/api/generate-targeting",
                            json=request_data,
                            timeout=60,
                        )

                        if response.status_code == 200:
                            st.session_state.generated_data = response.json()
                            st.success("Success! Your audience intelligence is ready.")
                            time.sleep(1)
                            st.session_state.current_page = "insights"
                            st.rerun()
                        else:
                            st.error(
                                f"Error: {response.status_code}. Please try again."
                            )

                    except Exception as e:
                        st.error(
                            "Connection failed. Please check your internet connection and try again."
                        )
