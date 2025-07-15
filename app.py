import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import time
import base64

# Configure Streamlit
st.set_page_config(
    page_title="TasteTarget | Enterprise AI Platform",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Professional Black & White CSS
st.markdown("""
<style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Reset and Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit Components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main App Background */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #000000;
        width: 280px !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Main Container */
    .main > div {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    /* Professional Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 900;
        color: #000000;
        letter-spacing: -0.03em;
        margin: 0;
        padding: 0;
        line-height: 1;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #666666;
        font-weight: 400;
        margin-top: 0.5rem;
        margin-bottom: 3rem;
        letter-spacing: -0.01em;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 1.5rem;
        letter-spacing: -0.02em;
        text-transform: uppercase;
        position: relative;
        padding-bottom: 0.75rem;
    }
    
    .section-header:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 3px;
        background-color: #000000;
    }
    
    /* Card Styles */
    .metric-card {
        background-color: #000000;
        color: #FFFFFF;
        padding: 2rem;
        border-radius: 0;
        height: 100%;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
    }
    
    .metric-card h4 {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 0;
        color: #999999;
    }
    
    .metric-card .value {
        font-size: 3rem;
        font-weight: 800;
        margin: 1rem 0 0 0;
        letter-spacing: -0.02em;
    }
    
    .metric-card .delta {
        font-size: 0.875rem;
        color: #CCCCCC;
        margin-top: 0.5rem;
    }
    
    /* Content Card */
    .content-card {
        background-color: #FAFAFA;
        border: 2px solid #000000;
        padding: 2.5rem;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .content-card:hover {
        background-color: #F5F5F5;
    }
    
    /* Persona Card */
    .persona-card {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        padding: 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        transition: all 0.2s ease;
    }
    
    .persona-card:hover {
        box-shadow: 8px 8px 0px #000000;
        transform: translate(-2px, -2px);
    }
    
    .persona-number {
        position: absolute;
        top: -20px;
        right: 20px;
        background-color: #000000;
        color: #FFFFFF;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.25rem;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #000000;
        color: #FFFFFF;
        border: none;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        transition: all 0.2s ease;
        border-radius: 0;
    }
    
    .stButton > button:hover {
        background-color: #FFFFFF;
        color: #000000;
        box-shadow: 0 0 0 2px #000000;
    }
    
    /* Secondary Button Style */
    [data-testid="stButton"] [kind="secondary"] > button {
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #000000;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 0;
        color: #000000;
        font-weight: 500;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #000000;
        box-shadow: 4px 4px 0px #000000;
        outline: none;
    }
    
    /* Select Boxes */
    .stSelectbox > div > div > div {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 0;
        color: #000000;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div > div {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 0;
    }
    
    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stMultiSelect > label {
        color: #000000;
        font-weight: 700;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #000000;
        padding: 0;
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #000000;
        color: #FFFFFF;
        border-radius: 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 1rem 2rem;
        border-right: 1px solid #333333;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #000000;
        color: #FFFFFF;
        border-radius: 0;
        font-weight: 700;
        padding: 1rem 1.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .streamlit-expanderContent {
        border: 2px solid #000000;
        border-top: none;
        background-color: #FAFAFA;
        padding: 2rem;
    }
    
    /* Tags/Pills */
    .tag {
        display: inline-block;
        background-color: #000000;
        color: #FFFFFF;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
    }
    
    .tag:hover {
        background-color: #FFFFFF;
        color: #000000;
        box-shadow: 0 0 0 2px #000000;
    }
    
    /* Copy Blocks */
    .copy-block {
        background-color: #F5F5F5;
        border-left: 4px solid #000000;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'Inter', monospace;
    }
    
    .copy-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #666666;
        margin-bottom: 0.5rem;
    }
    
    /* Grid Lines */
    .grid-line {
        height: 1px;
        background-color: #E5E5E5;
        margin: 2rem 0;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: #000000;
        color: #FFFFFF;
        border-radius: 0;
        padding: 1rem;
        font-weight: 600;
    }
    
    .stError {
        background-color: #FF0000;
        color: #FFFFFF;
        border-radius: 0;
        padding: 1rem;
        font-weight: 600;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background-color: #000000;
    }
    
    /* Dataframe Styling */
    .dataframe {
        border: 2px solid #000000;
        font-size: 0.875rem;
    }
    
    .dataframe thead tr th {
        background-color: #000000;
        color: #FFFFFF;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 1rem;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #FAFAFA;
    }
    
    /* Loading Spinner */
    .stSpinner {
        color: #000000;
    }
    
    /* Metric Display */
    [data-testid="metric-container"] {
        background-color: #000000;
        padding: 1.5rem;
        border-radius: 0;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: #999999;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.75rem;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #FFFFFF;
        font-weight: 800;
        font-size: 2rem;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #000000;
        font-weight: 700;
    }
    
    .stDownloadButton > button:hover {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Code Block */
    .stCodeBlock {
        background-color: #000000;
        border-radius: 0;
    }
    
    /* Info Box */
    .stInfo {
        background-color: #F5F5F5;
        border-left: 4px solid #000000;
        border-radius: 0;
        color: #000000;
    }
    
    /* Warning Box */
    .stWarning {
        background-color: #FFF3CD;
        border-left: 4px solid #000000;
        border-radius: 0;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def generate_report(data: Dict) -> str:
    """Generate a minimalist professional report"""
    report = f"""TASTETARGET INTELLIGENCE REPORT
{'-' * 50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Product: {data['product_name']}

AUDIENCE SEGMENTS
{'-' * 50}"""
    
    for i, persona in enumerate(data['personas'], 1):
        report += f"""

{i}. {persona['name'].upper()}
{persona['description']}

Psychographics:
{chr(10).join(f'• {trait}' for trait in persona['psychographics'])}

Channels:
{chr(10).join(f'• {channel}' for channel in persona['preferred_channels'])}
"""
    
    report += f"""

MESSAGING STRATEGY
{'-' * 50}"""
    
    for copy in data['campaign_copies']:
        persona_name = next((p['name'] for p in data['personas'] 
                           if p['persona_id'] == copy['persona_id']), "Unknown")
        report += f"""

{persona_name.upper()}:
Tagline: {copy['tagline']}
Social: {copy['social_caption']}
Email: {copy['email_subject']}
"""
    
    return report

# Initialize session state
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None
if 'loading' not in st.session_state:
    st.session_state.loading = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'generate'

# Backend API URL
API_URL = st.secrets.get("API_URL", "http://localhost:8000")

# Minimal Navigation Bar
col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
with col1:
    st.markdown("""
        <h1 class="main-header">TASTETARGET</h1>
        <p class="sub-header">AI-POWERED AUDIENCE INTELLIGENCE</p>
    """, unsafe_allow_html=True)

with col2:
    if st.button("GENERATE", key="nav_generate", use_container_width=True):
        st.session_state.current_page = 'generate'

with col3:
    if st.button("ANALYZE", key="nav_analyze", use_container_width=True):
        st.session_state.current_page = 'analyze'

with col4:
    if st.button("EXPORT", key="nav_export", use_container_width=True):
        st.session_state.current_page = 'export'

with col5:
    if st.button("SETTINGS", key="nav_settings", use_container_width=True):
        st.session_state.current_page = 'settings'

st.markdown('<div class="grid-line"></div>', unsafe_allow_html=True)

# Main Content Based on Current Page
if st.session_state.current_page == 'generate':
    # Input Section with Clean Layout
    st.markdown('<h2 class="section-header">Product Configuration</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        product_name = st.text_input(
            "PRODUCT NAME",
            placeholder="Enter product name",
            key="product_name_input"
        )
        
        product_description = st.text_area(
            "PRODUCT DESCRIPTION",
            placeholder="Describe your product in detail...",
            height=150,
            key="product_desc_input"
        )
        
        campaign_tone = st.select_slider(
            "CAMPAIGN TONE",
            options=["MINIMAL", "BALANCED", "EXPRESSIVE", "BOLD"],
            value="BALANCED",
            key="tone_slider"
        )
    
    with col2:
        brand_values = st.multiselect(
            "BRAND VALUES",
            options=["SUSTAINABILITY", "INNOVATION", "QUALITY", "AUTHENTICITY", 
                     "MINIMALISM", "LUXURY", "ACCESSIBILITY", "CRAFT", 
                     "TRANSPARENCY", "COMMUNITY"],
            key="brand_values_input"
        )
        
        target_mood = st.multiselect(
            "TARGET MOOD",
            options=["CONSCIOUS", "MODERN", "BOLD", "SOPHISTICATED", 
                     "AUTHENTIC", "MINDFUL", "CREATIVE", "PROFESSIONAL"],
            key="target_mood_input"
        )
        
        # Advanced Settings in Minimal Expander
        with st.expander("ADVANCED SETTINGS"):
            include_analytics = st.checkbox("Include Analytics", value=True)
            export_format = st.selectbox(
                "Export Format",
                ["PDF", "JSON", "CSV", "POWERPOINT"]
            )
    
    # Generate Button
    st.markdown('<div class="grid-line"></div>', unsafe_allow_html=True)
    
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
                        st.error("CONNECTION FAILED")
                        st.session_state.loading = False

elif st.session_state.current_page == 'analyze' and st.session_state.generated_data:
    data = st.session_state.generated_data
    
    # Metrics Section
    st.markdown('<h2 class="section-header">Performance Metrics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>SEGMENTS</h4>
            <div class="value">{len(data['personas'])}</div>
            <div class="delta">IDENTIFIED</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>MESSAGES</h4>
            <div class="value">{len(data['campaign_copies'])}</div>
            <div class="delta">VARIATIONS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_insights = sum(len(p['cultural_interests']) for p in data['personas'])
        st.markdown(f"""
        <div class="metric-card">
            <h4>INSIGHTS</h4>
            <div class="value">{total_insights}</div>
            <div class="delta">DISCOVERED</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4>EFFICIENCY</h4>
            <div class="value">14X</div>
            <div class="delta">FASTER</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="grid-line"></div>', unsafe_allow_html=True)
    
    # Tabbed Content
    tab1, tab2, tab3, tab4 = st.tabs(["PERSONAS", "MESSAGING", "ANALYTICS", "STRATEGY"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Audience Personas</h2>', unsafe_allow_html=True)
        
        for i, persona in enumerate(data['personas']):
            st.markdown(f"""
            <div class="persona-card">
                <div class="persona-number">{i+1}</div>
                <h3 style="margin: 0 0 1rem 0; font-weight: 800;">{persona['name'].upper()}</h3>
                <p style="color: #666; margin-bottom: 2rem;">{persona['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**PSYCHOGRAPHICS**")
                for trait in persona['psychographics']:
                    st.markdown(f"<span class='tag'>{trait}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**CHANNELS**")
                for channel in persona['preferred_channels']:
                    st.markdown(f"<span class='tag'>{channel}</span>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("**INFLUENCERS**")
                for inf in persona['influencer_types']:
                    st.markdown(f"<span class='tag'>{inf}</span>", unsafe_allow_html=True)
            
            st.markdown("")
    
    with tab2:
        st.markdown('<h2 class="section-header">Campaign Messaging</h2>', unsafe_allow_html=True)
        
        for i, copy in enumerate(data['campaign_copies']):
            persona_name = next((p['name'] for p in data['personas'] 
                               if p['persona_id'] == copy['persona_id']), f"Persona {i+1}")
            
            with st.expander(f"{persona_name.upper()}", expanded=(i==0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="copy-block">
                        <div class="copy-label">TAGLINE</div>
                        {copy['tagline']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="copy-block">
                        <div class="copy-label">SOCIAL MEDIA</div>
                        {copy['social_caption']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="copy-block">
                        <div class="copy-label">EMAIL SUBJECT</div>
                        {copy['email_subject']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="copy-block">
                        <div class="copy-label">AD COPY</div>
                        {copy['ad_copy']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="section-header">Data Visualization</h2>', unsafe_allow_html=True)
        
        # Minimal black and white charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Interest distribution
            all_interests = {}
            for persona in data['personas']:
                for category, interests in persona['cultural_interests'].items():
                    if category not in all_interests:
                        all_interests[category] = 0
                    all_interests[category] += len(interests)
            
            fig = go.Figure(data=[go.Bar(
                x=list(all_interests.keys()),
                y=list(all_interests.values()),
                marker_color='black'
            )])
            fig.update_layout(
                title="INTEREST DISTRIBUTION",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif", color="black"),
                showlegend=False,
                height=400,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#E5E5E5')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Persona complexity
            persona_scores = []
            for persona in data['personas']:
                score = (len(persona['psychographics']) + 
                        len(persona['preferred_channels']) + 
                        sum(len(v) for v in persona['cultural_interests'].values()))
                persona_scores.append({
                    'name': persona['name'],
                    'score': score
                })
            
            df = pd.DataFrame(persona_scores)
            fig2 = go.Figure(data=[go.Bar(
                x=df['name'],
                y=df['score'],
                marker_color=['black', '#666666', '#999999']
            )])
            fig2.update_layout(
                title="PERSONA COMPLEXITY SCORE",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Inter, sans-serif", color="black"),
                showlegend=False,
                height=400,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#E5E5E5')
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab4:
        st.markdown('<h2 class="section-header">Strategic Recommendations</h2>', unsafe_allow_html=True)
        
        suggestions = data['suggestions']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**CONTENT THEMES**")
            for theme in suggestions.get('content_themes', []):
                st.markdown(f"<span class='tag'>{theme}</span>", unsafe_allow_html=True)
            
            st.markdown("<br>**PARTNERSHIPS**", unsafe_allow_html=True)
            for idea in suggestions.get('partnership_ideas', []):
                st.markdown(f"<span class='tag'>{idea}</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("**CAMPAIGN ANGLES**")
            for angle in suggestions.get('campaign_angles', []):
                st.markdown(f"<span class='tag'>{angle}</span>", unsafe_allow_html=True)
            
            st.markdown("<br>**VISUAL DIRECTION**", unsafe_allow_html=True)
            for direction in suggestions.get('visual_directions', []):
                st.markdown(f"<span class='tag'>{direction}</span>", unsafe_allow_html=True)

elif st.session_state.current_page == 'export' and st.session_state.generated_data:
    st.markdown('<h2 class="section-header">Export Options</h2>', unsafe_allow_html=True)
    
    data = st.session_state.generated_data
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### DOCUMENTS")
        
        # Text Report
        report = generate_report(data)
        st.download_button(
            label="DOWNLOAD REPORT",
            data=report,
            file_name=f"TasteTarget_{data['product_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        # JSON Export
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="EXPORT JSON",
            data=json_str,
            file_name=f"TasteTarget_{data['product_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.markdown("### SHARING")
        
        if st.button("GENERATE LINK", use_container_width=True):
            st.code("tastetarget.ai/share/ABC123XYZ")
        
        if st.button("EMAIL REPORT", use_container_width=True):
            st.info("Email functionality coming soon")
    
    with col3:
        st.markdown("### INTEGRATIONS")
        
        if st.button("EXPORT TO CRM", use_container_width=True):
            st.info("CRM integration coming soon")
        
        if st.button("EXPORT TO ADS", use_container_width=True):
            st.info("Ad platform integration coming soon")

elif st.session_state.current_page == 'settings':
    st.markdown('<h2 class="section-header">Settings</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ACCOUNT")
        st.text_input("COMPANY NAME", value="", placeholder="Enter company name")
        st.text_input("EMAIL", value="", placeholder="Enter email")
        st.selectbox("TIMEZONE", ["UTC", "EST", "PST", "CST"])
        
    with col2:
        st.markdown("### API CONFIGURATION")
        st.text_input("API KEY", value="****-****-****", type="password")
        if st.button("REGENERATE KEY", use_container_width=True):
            st.success("NEW KEY GENERATED")
        
        st.markdown("### PREFERENCES")
        st.checkbox("AUTO-EXPORT REPORTS", value=True)
        st.checkbox("EMAIL NOTIFICATIONS", value=False)

# If no data is available on analyze/export pages
elif st.session_state.current_page in ['analyze', 'export'] and not st.session_state.generated_data:
    st.markdown('<h2 class="section-header">No Data Available</h2>', unsafe_allow_html=True)
    st.info("Generate a campaign first to access this section.")
    if st.button("GO TO GENERATOR", use_container_width=True):
        st.session_state.current_page = 'generate'
        st.rerun()

# Minimal Footer
st.markdown('<div class="grid-line" style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <p style='color: #000000; font-weight: 600; font-size: 0.875rem; letter-spacing: 0.1em;'>
        TASTETARGET © 2024
    </p>
    <p style='color: #666666; font-size: 0.75rem; margin-top: 0.5rem;'>
        AI-POWERED AUDIENCE INTELLIGENCE
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Content (Hidden by default, minimal when opened)
with st.sidebar:
    st.markdown("""
    <div style='padding: 2rem 0;'>
        <h2 style='color: white; font-weight: 900; font-size: 1.5rem; margin-bottom: 2rem;'>TASTETARGET</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### QUICK LINKS")
    
    if st.button("◐ DASHBOARD", use_container_width=True, key="side_dash"):
        st.session_state.current_page = 'generate'
        st.rerun()
    
    if st.button("◑ HISTORY", use_container_width=True, key="side_hist"):
        st.info("Coming soon")
    
    if st.button("◒ SUPPORT", use_container_width=True, key="side_support"):
        st.info("support@tastetarget.ai")
    
    st.markdown("---")
    
    st.markdown("""
    <div style='position: absolute; bottom: 2rem; left: 1rem; right: 1rem;'>
        <p style='color: #666666; font-size: 0.75rem; text-align: center;'>
            VERSION 1.0.0<br>
            ENTERPRISE EDITION
        </p>
    </div>
    """, unsafe_allow_html=True)