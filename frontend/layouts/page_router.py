# frontend/layouts/page_router.py
import streamlit as st

from backend.utils.logger import configure_logging
from layouts.generate_layout import GeneratePage
from layouts.analyze_layout import AnalyzePage
from layouts.export_layout import ExportPage
from layouts.settings_layout import SettingsPage
from layouts.fallback_layout import FallbackPage
from layouts.dashboard_layout import DashboardPage
from layouts.library_layout import LibraryPage
from layouts.insights_layout import InsightsPage


class PageController:
    @staticmethod
    def render():
        # Ensure current_page is set only once on startup
        if "current_page" not in st.session_state:
            st.session_state.current_page = "dashboard"

        page = st.session_state.current_page
        data = st.session_state.get("generated_data")

        if page == "generate":
            GeneratePage.render()

        elif page == "dashboard":
            DashboardPage.render()

        elif page == "insights":
            if data:
                InsightsPage.render(data)
            else:
                st.markdown("## AUDIENCE INSIGHTS")
                st.info(
                    "No insights available. Generate a new campaign to see AI-powered audience intelligence."
                )
                if st.button("GO TO CAMPAIGN GENERATOR", type="primary"):
                    st.session_state.current_page = "generate"
                    st.rerun()

        elif page == "library":
            LibraryPage.render()

        elif page == "settings":
            SettingsPage.render()
        else:
            FallbackPage.render()
