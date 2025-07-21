import streamlit as st

def render_navigation():
    st.sidebar.markdown("## 📊 TasteTarget")
    st.sidebar.markdown("AI-Powered Audience Intelligence")

    if st.sidebar.button("🎨 Dashboard", key="nav_dashboard"):
        st.session_state.current_page = 'dashboard'

    if st.sidebar.button("🛠 Generate", key="nav_generate"):
        st.session_state.current_page = 'generate'

    if st.sidebar.button("📈 Analyze", key="nav_analyze"):
        st.session_state.current_page = 'analyze'

    if st.sidebar.button("📤 Export", key="nav_export"):
        st.session_state.current_page = 'export'

    if st.sidebar.button("⚙️ Settings", key="nav_settings"):
        st.session_state.current_page = 'settings'
    
    st.sidebar.markdown("---")