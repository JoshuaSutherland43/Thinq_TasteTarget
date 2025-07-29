import streamlit as st


def render_navigation():
    st.sidebar.markdown("## 📊 TasteTarget")
    st.sidebar.markdown("AI-Powered Audience Intelligence")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### YOUR WORKSPACE")

    # Company customization
    company_name = st.sidebar.text_input(
        "Company Name",
        value=st.session_state.get("company_name", "Your Company"),
        key="company_name",
    )
    st.sidebar.markdown("---")

    if st.sidebar.button(" DASHBOARD", key="nav_dashboard"):
        st.session_state.current_page = "dashboard"

    if st.sidebar.button(" CAMPAIGN GENERATOR", key="nav_generate"):
        st.session_state.current_page = "generate"

    if st.sidebar.button(" AUDIENCE INSIGHTS", key="nav_insights"):
        st.session_state.current_page = "insights"

    if st.sidebar.button(" CAMPAIGN LIBRARY", key="nav_library"):
        st.session_state.current_page = "library"

    if st.sidebar.button("⚙️ Settings", key="nav_settings"):
        st.session_state.current_page = "settings"

    st.sidebar.markdown("---")

    # Quick Stats
    st.sidebar.markdown("### QUICK STATS")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.sidebar.metric("Campaigns", "12", "+3")
    with col2:
        st.sidebar.metric("Segments", "36", "+8")

    st.sidebar.markdown("---")

    # Help Section
    with st.sidebar.expander("NEED HELP?"):
        st.sidebar.markdown(
            """
        **Getting Started:**
        1. Enter your product details
        2. Select brand values and target mood
        3. Generate AI insights
        4. Export and implement
        
        **Support:**
        - Email: support@tastetarget.ai
        - Phone: 1-800-TASTE-AI
        - Live chat available
        """
        )
