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
from frontend.components.navigation import render_navigation
from frontend.themes.style_manager import get_stylesheet
from frontend.layouts.page_router import PageController as LayoutPageController


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

