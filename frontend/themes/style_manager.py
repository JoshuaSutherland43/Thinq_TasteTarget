from pathlib import Path
import streamlit as st

def get_stylesheet():
    css_path = Path(__file__).parent / "stylesheet.css"
    with css_path.open() as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)