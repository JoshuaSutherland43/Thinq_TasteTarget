import streamlit as st
import pandas as pd
from builders.current_form import current_form
from components.buttons import generate_btn
from components.sidebar import Sidebar

API_URL = st.secrets["API_URL"]


class DashboardPage:
    @staticmethod
    def render():
        st.title(" TasteTarget Dashboard")
        st.markdown("## MARKETING INTELLIGENCE DASHBOARD")

        # Value Proposition Section
        with st.container():
            st.markdown(
                """
            <div class="value-prop">
                <h3>Why TasteTarget is Different</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 3rem;">
                    <div>
                        <h4>Traditional Marketing</h4>
                        <ul>
                            <li>Demographics-based (age, gender)</li>
                            <li>Generic personas</li>
                            <li>Broad channel strategies</li>
                            <li>2-4 weeks to develop</li>
                            <li>Static insights</li>
                        </ul>
                    </div>
                    <div>
                        <h4>TasteTarget Intelligence</h4>
                        <ul>
                            <li>Cultural & behavioral insights</li>
                            <li>AI-powered precision personas</li>
                            <li>Channel-specific strategies</li>
                            <li>Results in 60 seconds</li>
                            <li>Real-time cultural data</li>
                        </ul>
                    </div>
                </div>
                <p>
                    We don't just tell you WHO your audience is - we show you HOW to reach them, 
                    WHAT to say, and WHERE to find them with actionable, implementation-ready strategies.
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")
        # Welcome Message
        st.info(
            "Welcome back. Your AI-powered marketing intelligence platform is ready to transform your campaigns."
        )

        # End of the modern container
        st.markdown("</div>", unsafe_allow_html=True)

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                """
            <div class="metric-card">
                <div class="value">89%</div>
                <div class="label">Campaign Success Rate</div>
                <div class="change">↑ 12% vs traditional methods</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
            <div class="metric-card">
                <div class="value">60sec</div>
                <div class="label">Time to Insights</div>
                <div class="change">↑ 99% faster</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                """
            <div class="metric-card">
                <div class="value">3.2x</div>
                <div class="label">ROI Improvement</div>
                <div class="change">↑ vs generic targeting</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                """
            <div class="metric-card">
                <div class="value">15+</div>
                <div class="label">Data Points Per Persona</div>
                <div class="change">↑ Actionable insights</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown(
            '<p class="navbar-subtitle">Your metrics at a glance</p>',
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📈 Campaigns", "12", "+3")
        with col2:
            st.metric("🧠 Segments", "36", "+8")

        # Recent Campaigns
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### RECENT CAMPAIGNS")
            campaigns_df = pd.DataFrame(
                {
                    "Campaign": [
                        "Summer Collection 2024",
                        "Eco-Friendly Launch",
                        "Holiday Special",
                    ],
                    "Date": ["2024-06-15", "2024-06-10", "2024-06-05"],
                    "Segments": [3, 4, 3],
                    "Performance": ["92%", "87%", "95%"],
                    "Status": ["Active", "Active", "Completed"],
                }
            )
            st.dataframe(campaigns_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("### QUICK ACTIONS")
            if st.button("NEW CAMPAIGN", use_container_width=True):
                st.session_state.current_page = "generate"
                st.rerun()

            if st.button("VIEW ANALYTICS", use_container_width=True):
                st.session_state.current_page = "insights"
                st.rerun()

            if st.button("EXPORT REPORTS", use_container_width=True):
                st.session_state.current_page = "insights"
                st.rerun()

            if st.button("SYNC DATA", use_container_width=True):
                st.session_state.current_page = "settings"
                st.rerun()

        if st.session_state.current_page == "generate":
            st.markdown("## CAMPAIGN GENERATOR")

            # Progress indicator
            progress_cols = st.columns(4)
            with progress_cols[0]:
                st.markdown("**1. PRODUCT INFO** ✓")
            with progress_cols[1]:
                st.markdown("**2. BRAND VALUES**")
            with progress_cols[2]:
                st.markdown("**3. TARGET AUDIENCE**")
            with progress_cols[3]:
                st.markdown("**4. GENERATE**")

        st.markdown("---")

        with st.expander("🆘 NEED HELP?"):
            st.markdown(
                """
                **Getting Started:**
                1. Enter your product details
                2. Select brand values and target mood
                3. Generate AI insights
                4. Export and implement

                **Support:**
                - 📧 Email: support@tastetarget.ai
                - 📞 Phone: 1-800-TASTE-AI
                - 💬 Live chat available
                """
            )
