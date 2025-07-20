# frontend/layouts/page_router.py
import streamlit as st

from frontend.layouts.generate_layout import GeneratePage
from frontend.layouts.analyze_layout import AnalyzePage
from frontend.layouts.export_layout import ExportPage
from frontend.layouts.settings_layout import SettingsPage
from frontend.layouts.fallback_layout import FallbackPage
from frontend.layouts.dashboard_layout import DashboardPage

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
        elif page == "analyze":
            if data:
                AnalyzePage.render(data)
            else:
                st.warning("No generated data available. Please generate first.")
        elif page == "export":
            if data:
                ExportPage.render(data)
            else:
                st.warning("No generated data available. Please generate first.")
        elif page == "settings":
            SettingsPage.render()
        else:
            FallbackPage.render()
