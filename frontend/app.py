import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Initialize Streamlit Configuration
st.set_page_config(
    page_title="TasteTarget | Enterprise AI Platform",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.state_management.app_state import get_session_state, AppState
from components.navigation import render_navigation
from themes.style_manager import get_stylesheet
from layouts.page_router import PageController as LayoutPageController


# Apply Stylesheet
get_stylesheet()

# Initialize session state
get_session_state(st.session_state)

# Initialize app state
state = AppState(st.session_state)

# Backend API URL
API_URL = st.secrets.get("API_URL", "http://localhost:8000")

# Render Navigation
render_navigation()

# Main Content - Use the PageController from layouts
LayoutPageController.render()

# Professional Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #666666;'>
    <p style='margin: 0;'>
        <strong>TASTETARGET</strong> - AI-Powered Audience Intelligence Platform<br>
        <span style='font-size: 0.875rem;'>
            Enterprise Marketing Solution | SOC 2 Compliant | GDPR Ready<br>
            © 2024 TasteTarget Inc. All rights reserved.
        </span>
    </p>
</div>
""", unsafe_allow_html=True)
