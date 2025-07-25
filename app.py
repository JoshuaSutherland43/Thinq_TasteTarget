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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit
st.set_page_config(
    page_title="TasteTarget - AI Marketing Intelligence",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://tastetarget.ai/help',
        'Report a bug': 'https://tastetarget.ai/support',
        'About': 'TasteTarget - AI-Powered Audience Intelligence Platform'
    }
)

# Professional Black & White CSS
st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FFFFFF;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main Container */
    .main {
        padding: 0;
        background-color: #FFFFFF;
    }
    
    /* Custom Header */
    .main-header {
        background: #000000;
        color: white;
        padding: 2.5rem 3rem;
        margin: -1rem -3rem 2rem -3rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.8;
        font-size: 1rem;
        font-weight: 400;
    }
    
    /* Cards */
    .card {
        background: white;
        border: 1px solid #E5E5E5;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
    }
    
    .card:hover {
        border-color: #000000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border: 2px solid #000000;
        padding: 2rem;
        text-align: center;
        transition: all 0.2s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        background: #000000;
        color: white;
    }
    
    .metric-card:hover .value,
    .metric-card:hover .label,
    .metric-card:hover .change {
        color: white !important;
    }
    
    .metric-card .value {
        font-size: 3rem;
        font-weight: 800;
        color: #000000;
        margin: 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .metric-card .label {
        font-size: 0.75rem;
        color: #666666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .metric-card .change {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 0.5rem;
        color: #000000;
    }
    
    /* Buttons */
    .stButton > button {
        background: #000000;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #FFFFFF;
        color: #000000;
        box-shadow: 0 0 0 2px #000000 inset;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 1px solid #CCCCCC;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        background-color: white;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #000000;
        box-shadow: none;
        outline: none;
    }
    
    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stMultiSelect > label {
        color: #000000;
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F5F5F5;
        padding: 0;
        gap: 0;
        border-bottom: 2px solid #000000;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #666666;
        font-weight: 600;
        padding: 1rem 2rem;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        color: #000000;
        border-bottom-color: #000000;
        background-color: white;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FAFAFA;
        border-right: 1px solid #E5E5E5;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: #000000;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F8F8F8;
        border: 1px solid #E5E5E5;
        font-weight: 600;
        color: #000000;
        padding: 1rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #000000;
        color: white;
        border-color: #000000;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: #F0F0F0;
        color: #000000;
        border-left: 4px solid #000000;
        font-weight: 500;
    }
    
    .stError {
        background-color: #000000;
        color: #FFFFFF;
        font-weight: 500;
    }
    
    /* Persona Cards */
    .persona-card {
        background: white;
        border: 2px solid #000000;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
    }
    
    .persona-card:hover {
        box-shadow: 6px 6px 0 #000000;
        transform: translate(-3px, -3px);
    }
    
    .persona-header {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .persona-avatar {
        width: 50px;
        height: 50px;
        background: #000000;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 800;
    }
    
    /* Tags */
    .tag {
        display: inline-block;
        background-color: #F0F0F0;
        color: #000000;
        padding: 0.375rem 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 1px solid #E5E5E5;
        transition: all 0.2s ease;
    }
    
    .tag:hover {
        background-color: #000000;
        color: white;
        border-color: #000000;
    }
    
    /* Copy Blocks */
    .copy-block {
        background-color: #FAFAFA;
        border-left: 3px solid #000000;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .copy-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    /* Section Headers */
    .section-header {
        color: #000000;
        font-size: 1.75rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #000000;
        text-transform: uppercase;
        letter-spacing: -0.02em;
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background-color: white;
        color: #000000;
        border: 2px solid #000000;
    }
    
    .stDownloadButton > button:hover {
        background-color: #000000;
        color: white;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background-color: #F8F8F8;
        padding: 1.5rem;
        border: 1px solid #E5E5E5;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #F8F8F8;
        border: 1px solid #E5E5E5;
        color: #000000;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        border: 1px solid #CCCCCC;
        background-color: white;
    }
    
    /* Select Slider */
    .stSelectSlider > div > div {
        background-color: #F8F8F8;
    }
    
    /* Data frames */
    .dataframe {
        border: 1px solid #E5E5E5;
    }
    
    .dataframe thead tr th {
        background-color: #000000 !important;
        color: white !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }
    
    /* Value Proposition Box */
    .value-prop {
        background: #000000;
        color: white;
        padding: 3rem;
        margin-bottom: 2rem;
    }
    
    .value-prop h3 {
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 2rem;
        text-transform: uppercase;
        letter-spacing: -0.02em;
    }
    
    .value-prop h4 {
        color: white;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .value-prop ul {
        opacity: 0.9;
        line-height: 1.8;
    }
    
    .value-prop p {
        margin-top: 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def generate_report(data: Dict) -> str:
    """Generate a professional marketing report"""
    report = f"""AUDIENCE INTELLIGENCE REPORT
=====================================
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Product: {data['product_name']}

EXECUTIVE SUMMARY
-----------------
This report provides AI-generated audience insights and marketing recommendations based on cultural intelligence analysis.

IDENTIFIED AUDIENCE SEGMENTS
----------------------------"""
    
    for i, persona in enumerate(data['personas'], 1):
        report += f"""

{i}. {persona['name']}
   Profile: {persona['description']}
   
   Key Characteristics:
   {chr(10).join(f'   • {trait}' for trait in persona['psychographics'])}
   
   Recommended Channels:
   {chr(10).join(f'   • {channel}' for channel in persona['preferred_channels'])}
"""
    
    report += """

MESSAGING STRATEGY
------------------"""
    
    for copy in data['campaign_copies']:
        persona_name = next((p['name'] for p in data['personas'] 
                           if p['persona_id'] == copy['persona_id']), "Unknown")
        report += f"""

{persona_name}:
• Tagline: {copy['tagline']}
• Social Media: {copy['social_caption']}
• Email Subject: {copy['email_subject']}
"""
    
    report += """

STRATEGIC RECOMMENDATIONS
-------------------------
Based on the analysis, we recommend focusing on the identified audience segments with tailored messaging across their preferred channels.

---
Report generated by TasteTarget AI Platform
"""
    
    return report

# Initialize session state
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None
if 'loading' not in st.session_state:
    st.session_state.loading = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

# Backend API URL
API_URL = st.secrets.get("API_URL", "http://localhost:8000")

# Header
st.markdown("""
<div class="main-header">
    <h1>TASTETARGET</h1>
    <p>AI-Powered Audience Intelligence for Modern Marketing Teams</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("### YOUR WORKSPACE")
    
    # Company customization
    company_name = st.text_input("Company Name", value="Your Company", key="company_name")
    
    st.markdown("---")
    
    st.markdown("### NAVIGATION")
    
    pages = {
        "dashboard": {"name": "Dashboard"},
        "generate": {"name": "Campaign Generator"},
        "insights": {"name": "Audience Insights"},
        "library": {"name": "Campaign Library"},
        "settings": {"name": "Settings"}
    }
    
    for page_id, page_info in pages.items():
        if st.button(page_info['name'].upper(), key=f"nav_{page_id}", use_container_width=True):
            st.session_state.current_page = page_id
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### QUICK STATS")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Campaigns", "12", "+3")
    with col2:
        st.metric("Segments", "36", "+8")
    
    st.markdown("---")
    
    # Help Section
    with st.expander("NEED HELP?"):
        st.markdown("""
        **Getting Started:**
        1. Enter your product details
        2. Select brand values and target mood
        3. Generate AI insights
        4. Export and implement
        
        **Support:**
        - Email: support@tastetarget.ai
        - Phone: 1-800-TASTE-AI
        - Live chat available
        """)

# Main Content Area
if st.session_state.current_page == 'dashboard':
    # Dashboard Overview
    st.markdown("## MARKETING INTELLIGENCE DASHBOARD")
    
    # Value Proposition Section
    with st.container():
        st.markdown("""
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
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Welcome Message
    st.info("Welcome back. Your AI-powered marketing intelligence platform is ready to transform your campaigns.")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="value">89%</div>
            <div class="label">Campaign Success Rate</div>
            <div class="change">↑ 12% vs traditional methods</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="value">60sec</div>
            <div class="label">Time to Insights</div>
            <div class="change">↑ 99% faster</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="value">3.2x</div>
            <div class="label">ROI Improvement</div>
            <div class="change">↑ vs generic targeting</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="value">15+</div>
            <div class="label">Data Points Per Persona</div>
            <div class="change">↑ Actionable insights</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Campaigns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### RECENT CAMPAIGNS")
        campaigns_df = pd.DataFrame({
            'Campaign': ['Summer Collection 2024', 'Eco-Friendly Launch', 'Holiday Special'],
            'Date': ['2024-06-15', '2024-06-10', '2024-06-05'],
            'Segments': [3, 4, 3],
            'Performance': ['92%', '87%', '95%'],
            'Status': ['Active', 'Active', 'Completed']
        })
        st.dataframe(campaigns_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### QUICK ACTIONS")
        if st.button("NEW CAMPAIGN", use_container_width=True):
            st.session_state.current_page = 'generate'
            st.rerun()
        
        st.button("VIEW ANALYTICS", use_container_width=True)
        st.button("EXPORT REPORTS", use_container_width=True)
        st.button("SYNC DATA", use_container_width=True)

elif st.session_state.current_page == 'generate':
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
    
    # Input Form
    with st.form("campaign_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### PRODUCT INFORMATION")
            product_name = st.text_input(
                "PRODUCT/CAMPAIGN NAME *",
                placeholder="e.g., Summer Collection 2024",
                help="Enter a memorable name for your product or campaign"
            )
            
            product_description = st.text_area(
                "DESCRIPTION *",
                placeholder="Describe your product, its features, benefits, and what makes it unique...",
                height=150,
                help="The more detail you provide, the better the AI can understand your product"
            )
            
            industry = st.selectbox(
                "INDUSTRY",
                ["Fashion & Retail", "Technology", "Food & Beverage", "Beauty & Wellness",
                 "Travel & Hospitality", "Financial Services", "Healthcare", "Education", "Other"]
            )
        
        with col2:
            st.markdown("### BRAND & AUDIENCE")
            brand_values = st.multiselect(
                "BRAND VALUES *",
                ["Sustainability", "Innovation", "Quality", "Authenticity", 
                 "Luxury", "Accessibility", "Creativity", "Trust", 
                 "Performance", "Community", "Heritage", "Simplicity"],
                help="Select up to 5 core values that represent your brand"
            )
            
            target_mood = st.multiselect(
                "TARGET AUDIENCE MINDSET *",
                ["Aspirational", "Practical", "Adventurous", "Sophisticated", 
                 "Eco-conscious", "Tech-savvy", "Traditional", "Trendy",
                 "Budget-conscious", "Premium-seeking", "Health-focused", "Social"],
                help="Select the mindsets that best describe your target audience"
            )
            
            campaign_tone = st.select_slider(
                "CAMPAIGN TONE",
                options=["Professional", "Friendly", "Playful", "Bold", "Inspirational"],
                value="Friendly",
                help="Choose the overall tone for your marketing messages"
            )
        
        # Advanced Options
        with st.expander("ADVANCED OPTIONS"):
            col1, col2 = st.columns(2)
            with col1:
                include_competitors = st.checkbox("Include competitor analysis", value=False)
                generate_visuals = st.checkbox("Generate visual guidelines", value=True)
            with col2:
                num_personas = st.slider("Number of personas", 2, 5, 3)
                languages = st.multiselect("Additional languages", ["Spanish", "French", "German", "Japanese"])
        
        # Submit Button
        submitted = st.form_submit_button("GENERATE AUDIENCE INTELLIGENCE", use_container_width=True)
    
    if submitted:
        if not all([product_name, product_description, brand_values, target_mood]):
            st.error("Please fill in all required fields marked with *")
        else:
            with st.spinner("AI is analyzing your product and generating insights..."):
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
                    "campaign_tone": campaign_tone.lower()
                }
                
                try:
                    response = requests.post(
                        f"{API_URL}/api/generate-targeting",
                        json=request_data,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        st.session_state.generated_data = response.json()
                        st.success("Success! Your audience intelligence is ready.")
                        time.sleep(1)
                        st.session_state.current_page = 'insights'
                        st.rerun()
                    else:
                        st.error(f"Error: {response.status_code}. Please try again.")
                        
                except Exception as e:
                    st.error("Connection failed. Please check your internet connection and try again.")

elif st.session_state.current_page == 'insights' and st.session_state.generated_data:
    data = st.session_state.generated_data
    
    # Validate data structure
    if not isinstance(data, dict):
        st.error("Invalid data format. Please regenerate the campaign.")
        st.stop()
    
    # Ensure required fields exist
    data['personas'] = data.get('personas', [])
    data['campaign_copies'] = data.get('campaign_copies', [])
    data['suggestions'] = data.get('suggestions', {})
    
    st.markdown(f"## AUDIENCE INSIGHTS: {data.get('product_name', 'Unknown Product').upper()}")
    
    # Summary Cards with error handling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Audience Segments", len(data['personas']), "AI-identified")
    with col2:
        st.metric("Message Variations", len(data['campaign_copies']), "Personalized")
    with col3:
        total_insights = 0
        for persona in data['personas']:
            if isinstance(persona, dict) and 'cultural_interests' in persona:
                for interests in persona['cultural_interests'].values():
                    if isinstance(interests, list):
                        total_insights += len(interests)
        st.metric("Cultural Insights", total_insights, "Data points")
    with col4:
        st.metric("Time Saved", "2 weeks", "vs manual research")
    
    # Tabbed Interface
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "AUDIENCE PERSONAS", 
        "MESSAGING", 
        "VISUALS",
        "ANALYTICS", 
        "RECOMMENDATIONS",
        "EXPORT"
    ])
    
    with tab1:
        st.markdown("### AI-IDENTIFIED AUDIENCE SEGMENTS")
        st.info("Click on any insight category below to see detailed implementation strategies tailored to your product.")
        
        for i, persona in enumerate(data['personas']):
            with st.container():
                st.markdown(f"""
                <div class="persona-card">
                    <div class="persona-header">
                        <div class="persona-avatar">{i+1}</div>
                        <div>
                            <h3 style="margin: 0; text-transform: uppercase;">{persona['name']}</h3>
                            <p style="margin: 0; color: #666666;">{persona['description']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Create tabs for detailed insights
                insight_tabs = st.tabs(["PSYCHOGRAPHICS", "CHANNELS", "INFLUENCERS", "CULTURAL PROFILE"])
                
                with insight_tabs[0]:
                    st.markdown("#### PSYCHOGRAPHIC ANALYSIS")
                    
                    # Create detailed psychographic profiles
                    psychographic_details = {
                        "thoughtful": {
                            "description": "Makes considered decisions, researches thoroughly before purchasing",
                            "triggers": ["Quality guarantees", "Detailed product information", "Expert reviews"],
                            "messaging": "Emphasize craftsmanship, provide comprehensive details, showcase expertise"
                        },
                        "quality-focused": {
                            "description": "Prioritizes excellence over price, seeks premium experiences",
                            "triggers": ["Premium materials", "Exclusive features", "Limited editions"],
                            "messaging": "Highlight superior quality, emphasize exclusivity, showcase premium aspects"
                        },
                        "authentic": {
                            "description": "Values genuine brands, seeks transparency and honesty",
                            "triggers": ["Behind-the-scenes content", "Founder stories", "Real customer testimonials"],
                            "messaging": "Be transparent about processes, share real stories, avoid corporate speak"
                        },
                        "innovative": {
                            "description": "Early adopter, excited by new technologies and approaches",
                            "triggers": ["New features", "Tech integration", "First-to-market claims"],
                            "messaging": "Emphasize innovation, highlight cutting-edge features, position as forward-thinking"
                        },
                        "conscious": {
                            "description": "Considers impact of purchases on society and environment",
                            "triggers": ["Sustainability metrics", "Social impact", "Ethical certifications"],
                            "messaging": "Lead with values, provide impact data, showcase certifications"
                        }
                    }
                    
                    for trait in persona['psychographics']:
                        with st.expander(f"**{trait.upper()}**", expanded=True):
                            detail = psychographic_details.get(trait.lower(), {
                                "description": f"Key personality trait influencing purchase decisions",
                                "triggers": ["Relevant messaging", "Aligned values", "Appropriate tone"],
                                "messaging": "Tailor content to resonate with this trait"
                            })
                            
                            st.markdown(f"**What this means:** {detail['description']}")
                            
                            st.markdown("**Purchase Triggers:**")
                            for trigger in detail['triggers']:
                                st.markdown(f"• {trigger}")
                            
                            st.markdown(f"**Messaging Strategy:** {detail['messaging']}")
                            
                            # Add specific examples for this product
                            st.markdown(f"**For {data['product_name']}:**")
                            st.markdown(f"• Feature {trait}-aligned benefits prominently")
                            st.markdown(f"• Use language that resonates with {trait} mindset")
                            st.markdown(f"• Create content that validates their {trait} nature")
                
                with insight_tabs[1]:
                    st.markdown("#### CHANNEL STRATEGY & IMPLEMENTATION")
                    
                    # Detailed channel strategies
                    channel_strategies = {
                        "Instagram": {
                            "best_practices": ["Visual storytelling", "Stories for behind-scenes", "Reels for product demos", "User-generated content"],
                            "content_types": ["Product photography", "Lifestyle shots", "Customer testimonials", "Educational carousels"],
                            "posting_schedule": "3-4 times per week, peak hours 11am-1pm and 7-9pm",
                            "hashtag_strategy": "Mix of branded, niche, and trending hashtags (10-15 per post)",
                            "engagement_tactics": ["Respond within 2 hours", "Use polls and questions", "Partner with micro-influencers"]
                        },
                        "Email": {
                            "best_practices": ["Personalized subject lines", "Segmented campaigns", "Mobile optimization", "Clear CTAs"],
                            "content_types": ["Welcome series", "Product education", "Exclusive offers", "Customer stories"],
                            "posting_schedule": "Weekly newsletter, bi-weekly promotional",
                            "segmentation": "By purchase history, engagement level, and interests",
                            "optimization": ["A/B test subject lines", "Optimize send times", "Monitor open rates"]
                        },
                        "YouTube": {
                            "best_practices": ["SEO-optimized titles", "Engaging thumbnails", "Consistent posting", "Community engagement"],
                            "content_types": ["Product demos", "How-to tutorials", "Brand story videos", "Customer testimonials"],
                            "posting_schedule": "1-2 videos per week, consistent day/time",
                            "optimization": ["Use cards and end screens", "Create playlists", "Collaborate with creators"],
                            "monetization": ["Affiliate programs", "Product placements", "YouTube Shopping"]
                        },
                        "LinkedIn": {
                            "best_practices": ["Thought leadership", "Industry insights", "Company culture", "B2B networking"],
                            "content_types": ["Industry articles", "Company updates", "Employee spotlights", "Case studies"],
                            "posting_schedule": "2-3 times per week, weekday mornings",
                            "engagement": ["Join industry groups", "Employee advocacy", "Executive thought leadership"],
                            "lead_generation": ["Gated content", "Webinars", "LinkedIn Lead Gen Forms"]
                        },
                        "TikTok": {
                            "best_practices": ["Trend participation", "Authentic content", "Quick hooks", "Sound selection"],
                            "content_types": ["Product reveals", "Behind-the-scenes", "Challenges", "Educational content"],
                            "posting_schedule": "Daily posting optimal, minimum 3-4 per week",
                            "growth_tactics": ["Collaborate with creators", "Use trending sounds", "Engage with comments"],
                            "advertising": ["Spark Ads", "In-feed ads", "Branded effects"]
                        }
                    }
                    
                    for channel in persona['preferred_channels']:
                        with st.expander(f"**{channel.upper()} STRATEGY**", expanded=True):
                            strategy = channel_strategies.get(channel, {
                                "best_practices": ["Platform-specific optimization", "Consistent branding", "Regular engagement"],
                                "content_types": ["Brand content", "User engagement", "Educational material"],
                                "posting_schedule": "Regular, consistent posting",
                                "optimization": ["Monitor analytics", "Test and iterate", "Engage with audience"]
                            })
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Best Practices:**")
                                for practice in strategy.get('best_practices', []):
                                    st.markdown(f"• {practice}")
                                
                                st.markdown("**Content Types:**")
                                for content in strategy.get('content_types', []):
                                    st.markdown(f"• {content}")
                            
                            with col2:
                                st.markdown(f"**Posting Schedule:** {strategy.get('posting_schedule', 'Customize based on audience')}")
                                
                                if 'hashtag_strategy' in strategy:
                                    st.markdown(f"**Hashtag Strategy:** {strategy['hashtag_strategy']}")
                                
                                if 'segmentation' in strategy:
                                    st.markdown(f"**Segmentation:** {strategy['segmentation']}")
                                
                                if 'engagement_tactics' in strategy:
                                    st.markdown("**Engagement Tactics:**")
                                    for tactic in strategy['engagement_tactics']:
                                        st.markdown(f"• {tactic}")
                            
                            # Channel-specific metrics
                            st.markdown("**Key Performance Indicators:**")
                            if channel == "Instagram":
                                st.markdown("• Engagement Rate: Target 3-6%")
                                st.markdown("• Story Views: 10-15% of followers")
                                st.markdown("• Profile Visits: Track weekly growth")
                            elif channel == "Email":
                                st.markdown("• Open Rate: Target 20-30%")
                                st.markdown("• Click Rate: Target 2-5%")
                                st.markdown("• Conversion Rate: Track by campaign")
                            elif channel == "YouTube":
                                st.markdown("• Watch Time: Maximize retention")
                                st.markdown("• CTR: Target 2-10%")
                                st.markdown("• Subscriber Growth: Track monthly")
                
                with insight_tabs[2]:
                    st.markdown("#### INFLUENCER PARTNERSHIP STRATEGY")
                    
                    # Detailed influencer strategies
                    influencer_strategies = {
                        "Micro-influencers": {
                            "follower_range": "1K - 100K followers",
                            "benefits": ["Higher engagement rates", "Niche audiences", "Cost-effective", "Authentic connections"],
                            "campaign_types": ["Product reviews", "Unboxing videos", "Day-in-life content", "Giveaways"],
                            "budget_range": "$100 - $10,000 per post",
                            "selection_criteria": ["Engagement rate > 3%", "Audience alignment", "Content quality", "Brand fit"]
                        },
                        "Industry experts": {
                            "follower_range": "Varies - credibility matters more than reach",
                            "benefits": ["Credibility boost", "Expert validation", "Thought leadership", "B2B influence"],
                            "campaign_types": ["Expert reviews", "Educational content", "Webinars", "White papers"],
                            "budget_range": "$1,000 - $50,000 per campaign",
                            "selection_criteria": ["Industry credentials", "Published work", "Speaking engagements", "Peer recognition"]
                        },
                        "Lifestyle creators": {
                            "follower_range": "10K - 1M+ followers",
                            "benefits": ["Lifestyle integration", "Visual storytelling", "Aspirational content", "Cross-platform reach"],
                            "campaign_types": ["Lifestyle integration", "Brand ambassadorships", "Content series", "Event coverage"],
                            "budget_range": "$500 - $100,000 per campaign",
                            "selection_criteria": ["Aesthetic alignment", "Audience demographics", "Content consistency", "Engagement quality"]
                        },
                        "Thought leaders": {
                            "follower_range": "Platform leaders regardless of size",
                            "benefits": ["Authority building", "Premium positioning", "Industry influence", "Long-term value"],
                            "campaign_types": ["Podcast appearances", "Article contributions", "Speaking engagements", "Advisory roles"],
                            "budget_range": "$5,000 - $200,000 per engagement",
                            "selection_criteria": ["Industry standing", "Media presence", "Network quality", "Alignment with brand values"]
                        }
                    }
                    
                    # Display specific influencer recommendations first
                    if hasattr(persona, 'specific_influencers') and persona.specific_influencers:
                        st.markdown("##### RECOMMENDED INFLUENCERS FOR YOUR BRAND")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if 'musicians' in persona.specific_influencers and persona.specific_influencers['musicians']:
                                st.markdown("**MUSICIANS & ARTISTS**")
                                for artist in persona.specific_influencers['musicians']:
                                    st.markdown(f"• **{artist}**")
                                st.markdown("")
                        
                        with col2:
                            if 'lifestyle_bloggers' in persona.specific_influencers and persona.specific_influencers['lifestyle_bloggers']:
                                st.markdown("**LIFESTYLE CREATORS**")
                                for blogger in persona.specific_influencers['lifestyle_bloggers']:
                                    st.markdown(f"• **{blogger}**")
                                st.markdown("")
                        
                        with col3:
                            if 'thought_leaders' in persona.specific_influencers and persona.specific_influencers['thought_leaders']:
                                st.markdown("**THOUGHT LEADERS**")
                                for leader in persona.specific_influencers['thought_leaders']:
                                    st.markdown(f"• **{leader}**")
                                st.markdown("")
                        
                        st.info("These are AI-recommended influencers based on your brand values and target audience's cultural interests. Verify their current status and alignment before reaching out.")
                        st.markdown("---")
                    
                    # Display general influencer strategies
                    st.markdown("##### INFLUENCER CATEGORY STRATEGIES")
                    
                    for inf_type in persona['influencer_types']:
                        with st.expander(f"**{inf_type.upper()}**", expanded=False):
                            strategy = influencer_strategies.get(inf_type, {
                                "follower_range": "Varies by platform",
                                "benefits": ["Increased reach", "Authentic endorsement", "Content creation"],
                                "campaign_types": ["Sponsored content", "Collaborations", "Brand partnerships"],
                                "budget_range": "Varies by scope",
                                "selection_criteria": ["Audience fit", "Engagement rate", "Content quality"]
                            })
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"**Typical Reach:** {strategy['follower_range']}")
                                st.markdown(f"**Budget Range:** {strategy['budget_range']}")
                                
                                st.markdown("**Key Benefits:**")
                                for benefit in strategy['benefits']:
                                    st.markdown(f"• {benefit}")
                                
                                st.markdown("**Campaign Types:**")
                                for campaign in strategy['campaign_types']:
                                    st.markdown(f"• {campaign}")
                            
                            with col2:
                                st.markdown("**Selection Criteria:**")
                                for criteria in strategy['selection_criteria']:
                                    st.markdown(f"• {criteria}")
                                
                                # Show specific examples if available
                                if hasattr(persona, 'specific_influencers') and persona.specific_influencers:
                                    relevant_examples = []
                                    
                                    if "micro" in inf_type.lower() and 'lifestyle_bloggers' in persona.specific_influencers:
                                        relevant_examples = persona.specific_influencers['lifestyle_bloggers'][:2]
                                    elif "expert" in inf_type.lower() and 'thought_leaders' in persona.specific_influencers:
                                        relevant_examples = persona.specific_influencers['thought_leaders'][:2]
                                    elif "lifestyle" in inf_type.lower() and 'lifestyle_bloggers' in persona.specific_influencers:
                                        relevant_examples = persona.specific_influencers['lifestyle_bloggers']
                                    elif "thought" in inf_type.lower() and 'thought_leaders' in persona.specific_influencers:
                                        relevant_examples = persona.specific_influencers['thought_leaders']
                                    
                                    if relevant_examples:
                                        st.markdown("**Specific Examples:**")
                                        for example in relevant_examples:
                                            st.markdown(f"• {example}")
                            
                            # Specific recommendations for this product
                            st.markdown(f"**Specific Recommendations for {data['product_name']}:**")
                            
                            # Generate contextual recommendations based on personas
                            if any("sustainab" in interest.lower() for interests in persona['cultural_interests'].values() for interest in interests):
                                st.markdown("• Partner with eco-conscious influencers who showcase sustainable lifestyles")
                                st.markdown("• Focus on creators who emphasize environmental impact in their content")
                            
                            if any("innovat" in interest.lower() or "tech" in interest.lower() for interests in persona['cultural_interests'].values() for interest in interests):
                                st.markdown("• Collaborate with tech-forward creators and early adopters")
                                st.markdown("• Seek partnerships with innovation-focused thought leaders")
                            
                            if any("luxury" in interest.lower() or "premium" in interest.lower() for interests in persona['cultural_interests'].values() for interest in interests):
                                st.markdown("• Engage premium lifestyle influencers with affluent audiences")
                                st.markdown("• Partner with creators known for luxury product reviews")
                            
                            # ROI tracking
                            st.markdown("**Measuring Success:**")
                            st.markdown("• Track using unique promo codes or affiliate links")
                            st.markdown("• Monitor engagement metrics (likes, comments, shares)")
                            st.markdown("• Measure traffic from influencer content")
                            st.markdown("• Calculate cost per acquisition from each partnership")
                
                with insight_tabs[3]:
                    st.markdown("#### CULTURAL INTEREST PROFILE")
                    
                    # Detailed breakdown of cultural interests
                    st.markdown("Understanding cultural interests helps create authentic connections with this audience segment.")
                    
                    for category, interests in persona['cultural_interests'].items():
                        with st.expander(f"**{category.upper()} PREFERENCES**", expanded=False):
                            st.markdown(f"**Top {category.title()} Interests:** {', '.join(interests[:5])}")
                            
                            # Provide actionable insights based on interests
                            st.markdown("**Marketing Applications:**")
                            
                            if category == "music":
                                st.markdown("• Use these music styles in video content and ads")
                                st.markdown("• Partner with artists in these genres")
                                st.markdown("• Sponsor concerts or festivals featuring these styles")
                                st.markdown("• Create playlists that resonate with this audience")
                            
                            elif category == "reading":
                                st.markdown("• Reference these topics in content marketing")
                                st.markdown("• Partner with publications in these categories")
                                st.markdown("• Create content that aligns with these interests")
                                st.markdown("• Advertise in relevant publications")
                            
                            elif category == "dining":
                                st.markdown("• Partner with these types of establishments")
                                st.markdown("• Host events at relevant venues")
                                st.markdown("• Create content around these dining experiences")
                                st.markdown("• Use food styling that matches these preferences")
                            
                            elif category == "travel":
                                st.markdown("• Feature these destinations in campaigns")
                                st.markdown("• Partner with travel brands in these categories")
                                st.markdown("• Create travel-themed content")
                                st.markdown("• Target ads to travelers interested in these destinations")
                            
                            elif category == "fashion":
                                st.markdown("• Align visual aesthetics with these styles")
                                st.markdown("• Partner with brands in these categories")
                                st.markdown("• Feature these fashion elements in campaigns")
                                st.markdown("• Collaborate with fashion influencers in these niches")
                            
                            # Cross-promotion opportunities
                            st.markdown("**Cross-Promotion Opportunities:**")
                            st.markdown(f"• Create {category}-themed campaigns that incorporate {data['product_name']}")
                            st.markdown(f"• Partner with {category} brands that share your values")
                            st.markdown(f"• Develop content that bridges {category} interests with your product")
    
    with tab2:
        st.markdown("### PERSONALIZED MESSAGING BY SEGMENT")
        
        for i, copy in enumerate(data['campaign_copies']):
            persona_name = next((p['name'] for p in data['personas'] 
                               if p['persona_id'] == copy['persona_id']), f"Segment {i+1}")
            
            with st.expander(f"{persona_name.upper()} - MESSAGING SUITE", expanded=(i==0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""<div class="copy-block">
                        <div class="copy-label">HERO TAGLINE</div>""", unsafe_allow_html=True)
                    st.write(copy['tagline'])
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("""<div class="copy-block">
                        <div class="copy-label">SOCIAL MEDIA CAPTION</div>""", unsafe_allow_html=True)
                    st.write(copy['social_caption'])
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("""<div class="copy-block">
                        <div class="copy-label">EMAIL SUBJECT LINE</div>""", unsafe_allow_html=True)
                    st.write(copy['email_subject'])
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""<div class="copy-block">
                        <div class="copy-label">DISPLAY AD COPY</div>""", unsafe_allow_html=True)
                    st.write(copy['ad_copy'])
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("""<div class="copy-block">
                        <div class="copy-label">PRODUCT DESCRIPTION</div>""", unsafe_allow_html=True)
                    st.write(copy['product_description'])
                    st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### AI-GENERATED MARKETING VISUALS")
        st.info("Generate custom marketing visuals tailored to each persona using AI. These visuals are optimized for your target audience's preferences.")
        
        # Visual style mapping based on persona characteristics
        style_mapping = {
            "eco_conscious": "natural organic",
            "tech_innovator": "tech futuristic",
            "premium_lifestyle": "luxury premium",
            "balanced_modern": "minimalist clean"
        }
        
        for i, persona in enumerate(data['personas']):
            with st.expander(f"{persona['name'].upper()} - VISUAL GENERATION", expanded=(i==0)):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("**VISUAL PARAMETERS**")
                    
                    # Auto-fill based on persona
                    persona_name = persona['name']
                    brand_values_str = ', '.join(data.get('brand_values', ['quality', 'innovation'])[:3])
                    product_desc = data.get('product_name', 'Product')
                    
                    # Determine style based on persona
                    default_style = style_mapping.get(persona.get('persona_id', ''), 'minimalist clean')
                    
                    # Style selector
                    style_preference = st.selectbox(
                        "Visual Style",
                        ["minimalist clean", "bold vibrant", "luxury premium", 
                         "natural organic", "tech futuristic", "artistic creative"],
                        index=["minimalist clean", "bold vibrant", "luxury premium", 
                               "natural organic", "tech futuristic", "artistic creative"].index(default_style),
                        key=f"visual_style_{persona.get('persona_id', i)}_{i}"
                    )
                    
                    # Additional customization
                    custom_elements = st.text_input(
                        "Additional Elements",
                        placeholder="e.g., urban background, nature elements",
                        key=f"visual_elements_{persona.get('persona_id', i)}_{i}"
                    )
                    
                    if st.button(f"GENERATE VISUAL", key=f"gen_visual_{persona.get('persona_id', i)}_{i}"):
                        with st.spinner("Generating visual..."):
                            try:
                                # Call the backend API
                                visual_request = {
                                    "persona_name": persona_name,
                                    "brand_values": brand_values_str,
                                    "product_description": f"{product_desc} {custom_elements}".strip(),
                                    "style_preference": style_preference
                                }
                                
                                response = requests.post(
                                    f"{API_URL}/api/generate-visual",
                                    json=visual_request,
                                    timeout=60
                                )
                                
                                if response.status_code == 200:
                                    result = response.json()
                                    if result['status'] == 'success' and result.get('image_data'):
                                        # Store in session state
                                        if 'generated_visuals' not in st.session_state:
                                            st.session_state.generated_visuals = {}
                                        st.session_state.generated_visuals[persona['persona_id']] = result['image_data']
                                        st.success("Visual generated successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to generate visual. Please try again.")
                                else:
                                    st.error(f"Error: {response.status_code}")
                                    
                            except Exception as e:
                                st.error(f"Generation failed: {str(e)}")
                                st.info("Note: Visual generation requires the backend API to be running.")
                
                with col2:
                    st.markdown("**GENERATED VISUAL**")
                    
                    # Display generated visual if available
                    if hasattr(st.session_state, 'generated_visuals') and persona['persona_id'] in st.session_state.generated_visuals:
                        image_data = st.session_state.generated_visuals[persona['persona_id']]
                        if image_data:
                            # Display the image
                            if image_data.startswith('data:image'):
                                # It's already a data URL
                                st.markdown(f'<img src="{image_data}" style="width: 100%; border: 2px solid #000;">', unsafe_allow_html=True)
                            else:
                                # It's base64 encoded
                                st.image(f"data:image/png;base64,{image_data}", use_column_width=True)
                            
                            # Download button
                            st.download_button(
                                label="DOWNLOAD IMAGE",
                                data=base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data),
                                file_name=f"{persona_name.replace(' ', '_')}_visual.png",
                                mime="image/png",
                                key=f"download_visual_{persona.get('persona_id', i)}_{i}"
                            )
                    else:
                        st.markdown("""
                        <div style="border: 2px dashed #CCCCCC; padding: 3rem; text-align: center; color: #666666;">
                            <p style="margin: 0;">No visual generated yet</p>
                            <p style="margin: 0.5rem 0 0 0; font-size: 0.875rem;">Click 'Generate Visual' to create one</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Visual usage guidelines
                    st.markdown("**USAGE GUIDELINES**")
                    st.markdown(f"""
                    • Use for {persona['preferred_channels'][0] if persona['preferred_channels'] else 'social media'} campaigns
                    • Adapt style for different platforms
                    • A/B test with your audience
                    • Maintain brand consistency
                    """)
        
        # Bulk generation option
        st.markdown("---")
        st.markdown("### BULK VISUAL GENERATION")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("GENERATE ALL VISUALS", use_container_width=True, key="bulk_generate_visuals"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, persona in enumerate(data['personas']):
                    status_text.text(f"Generating visual for {persona['name']}...")
                    progress_bar.progress((i + 1) / len(data['personas']))
                    
                    # Skip if already generated
                    if hasattr(st.session_state, 'generated_visuals') and persona['persona_id'] in st.session_state.generated_visuals:
                        continue
                    
                    try:
                        visual_request = {
                            "persona_name": persona['name'],
                            "brand_values": ', '.join(data.get('brand_values', ['quality'])[:3]),
                            "product_description": data.get('product_name', 'Product'),
                            "style_preference": style_mapping.get(persona.get('persona_id', ''), 'minimalist clean')
                        }
                        
                        response = requests.post(
                            f"{API_URL}/api/generate-visual",
                            json=visual_request,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            if result['status'] == 'success' and result.get('image_data'):
                                if 'generated_visuals' not in st.session_state:
                                    st.session_state.generated_visuals = {}
                                st.session_state.generated_visuals[persona['persona_id']] = result['image_data']
                        
                        time.sleep(1)  # Rate limiting
                        
                    except Exception as e:
                        logger.error(f"Bulk generation error for {persona['name']}: {e}")
                
                status_text.text("Visual generation complete!")
                progress_bar.progress(1.0)
                time.sleep(1)
                st.rerun()
    
    with tab4:
        st.markdown("### ANALYTICS & INSIGHTS")
        st.markdown("### ANALYTICS & INSIGHTS")
        
        # Check if we have data to analyze
        if data and 'personas' in data and len(data['personas']) > 0:
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Interest Distribution
                all_interests = {}
                for persona in data['personas']:
                    if 'cultural_interests' in persona:
                        for category, interests in persona['cultural_interests'].items():
                            if category not in all_interests:
                                all_interests[category] = 0
                            all_interests[category] += len(interests) if isinstance(interests, list) else 0
                
                if all_interests:
                    # Create pie chart only if we have data
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=[cat.title() for cat in all_interests.keys()],
                        values=list(all_interests.values()),
                        hole=.4,
                        marker=dict(colors=['#000000', '#333333', '#666666', '#999999', '#CCCCCC']),
                        textfont=dict(color='white', size=12)
                    )])
                    fig_pie.update_layout(
                        title={
                            'text': "INTEREST CATEGORY DISTRIBUTION",
                            'font': {'size': 14, 'family': 'Inter, sans-serif', 'color': '#000000'}
                        },
                        font=dict(family="Inter, sans-serif"),
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        height=400,
                        showlegend=True,
                        legend=dict(
                            font=dict(size=10),
                            orientation="v",
                            yanchor="middle",
                            y=0.5,
                            xanchor="left",
                            x=1.05
                        ),
                        margin=dict(l=20, r=120, t=40, b=20)
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No interest data available for visualization")
            
            with col2:
                # Persona Complexity
                persona_data = []
                for persona in data['personas']:
                    try:
                        # Calculate complexity score with error handling
                        psychographics_count = len(persona.get('psychographics', [])) if isinstance(persona.get('psychographics'), list) else 0
                        channels_count = len(persona.get('preferred_channels', [])) if isinstance(persona.get('preferred_channels'), list) else 0
                        
                        interests_count = 0
                        if 'cultural_interests' in persona and isinstance(persona['cultural_interests'], dict):
                            for interests in persona['cultural_interests'].values():
                                if isinstance(interests, list):
                                    interests_count += len(interests)
                        
                        score = psychographics_count + channels_count + interests_count
                        
                        persona_data.append({
                            'Persona': persona.get('name', 'Unknown'),
                            'Complexity Score': score
                        })
                    except Exception as e:
                        logger.error(f"Error calculating complexity for persona: {e}")
                        continue
                
                if persona_data:
                    df = pd.DataFrame(persona_data)
                    
                    # Create bar chart
                    fig_bar = go.Figure(data=[go.Bar(
                        x=df['Persona'],
                        y=df['Complexity Score'],
                        marker=dict(color='#000000'),
                        text=df['Complexity Score'],
                        textposition='outside',
                        textfont=dict(size=12, color='#000000')
                    )])
                    fig_bar.update_layout(
                        title={
                            'text': "AUDIENCE SEGMENT COMPLEXITY ANALYSIS",
                            'font': {'size': 14, 'family': 'Inter, sans-serif', 'color': '#000000'}
                        },
                        xaxis_title="Audience Segment",
                        yaxis_title="Complexity Score",
                        font=dict(family="Inter, sans-serif", size=10),
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        height=400,
                        showlegend=False,
                        xaxis=dict(tickangle=-45),
                        yaxis=dict(gridcolor='#E5E5E5', gridwidth=1),
                        margin=dict(l=40, r=40, t=60, b=80)
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No persona data available for complexity analysis")
            
            # Additional Analytics
            st.markdown("### DETAILED METRICS")
            
            # Create metrics based on actual data
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                # Calculate total reach potential
                total_channels = set()
                for persona in data.get('personas', []):
                    if 'preferred_channels' in persona and isinstance(persona['preferred_channels'], list):
                        total_channels.update(persona['preferred_channels'])
                
                st.metric(
                    label="UNIQUE CHANNELS",
                    value=len(total_channels),
                    delta="Distribution channels"
                )
                
                # List channels
                if total_channels:
                    st.markdown("**Available Channels:**")
                    for channel in sorted(total_channels):
                        st.markdown(f"• {channel}")
            
            with metrics_col2:
                # Calculate psychographic diversity
                all_psychographics = set()
                for persona in data.get('personas', []):
                    if 'psychographics' in persona and isinstance(persona['psychographics'], list):
                        all_psychographics.update(persona['psychographics'])
                
                st.metric(
                    label="PSYCHOGRAPHIC TRAITS",
                    value=len(all_psychographics),
                    delta="Unique traits"
                )
                
                # List top traits
                if all_psychographics:
                    st.markdown("**Key Traits:**")
                    for trait in sorted(list(all_psychographics))[:5]:
                        st.markdown(f"• {trait.title()}")
            
            with metrics_col3:
                # Calculate influencer types
                all_influencers = set()
                for persona in data.get('personas', []):
                    if 'influencer_types' in persona and isinstance(persona['influencer_types'], list):
                        all_influencers.update(persona['influencer_types'])
                
                st.metric(
                    label="INFLUENCER CATEGORIES",
                    value=len(all_influencers),
                    delta="Partnership types"
                )
                
                # List influencer types
                if all_influencers:
                    st.markdown("**Influencer Types:**")
                    for inf_type in sorted(all_influencers):
                        st.markdown(f"• {inf_type}")
            
            # Key Performance Indicators Table
            st.markdown("### KEY PERFORMANCE INDICATORS")
            
            # Create KPI data based on actual metrics
            kpi_data = {
                'Metric': [
                    'Audience Segments Identified',
                    'Personalized Messages Created',
                    'Channel Strategies Defined',
                    'Cultural Data Points Analyzed'
                ],
                'Value': [
                    len(data.get('personas', [])),
                    len(data.get('campaign_copies', [])),
                    len(total_channels),
                    sum(len(p.get('cultural_interests', {}).get(cat, [])) 
                        for p in data.get('personas', []) 
                        for cat in ['music', 'reading', 'dining', 'travel', 'fashion'])
                ],
                'Industry Benchmark': [
                    '2-3',
                    '2-3',
                    '3-4',
                    '10-15'
                ],
                'Performance': [
                    'Above' if len(data.get('personas', [])) >= 3 else 'At Par',
                    'Above' if len(data.get('campaign_copies', [])) >= 3 else 'At Par',
                    'Above' if len(total_channels) >= 4 else 'At Par',
                    'Above'
                ]
            }
            
            kpi_df = pd.DataFrame(kpi_data)
            
            # Style the dataframe
            def style_performance(val):
                if val == 'Above':
                    return 'color: #000000; font-weight: bold'
                return 'color: #666666'
            
            styled_df = kpi_df.style.applymap(style_performance, subset=['Performance'])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # Engagement Prediction Chart
            st.markdown("### PREDICTED ENGAGEMENT BY CHANNEL")
            
            # Create channel engagement data
            channel_data = []
            for persona in data.get('personas', []):
                persona_name = persona.get('name', 'Unknown')
                for channel in persona.get('preferred_channels', []):
                    # Assign predicted engagement based on channel type
                    engagement_rates = {
                        'Instagram': 3.5,
                        'TikTok': 4.2,
                        'YouTube': 2.8,
                        'Email': 25.0,
                        'LinkedIn': 2.2,
                        'Twitter': 1.8,
                        'Facebook': 1.5
                    }
                    base_rate = engagement_rates.get(channel, 2.0)
                    # Add some variation based on persona
                    variation = hash(persona_name + channel) % 20 / 10 - 1  # -1 to +1
                    rate = base_rate + variation
                    
                    channel_data.append({
                        'Channel': channel,
                        'Persona': persona_name,
                        'Predicted Engagement %': max(0.5, rate)
                    })
            
            if channel_data:
                channel_df = pd.DataFrame(channel_data)
                
                # Create grouped bar chart
                fig_engagement = px.bar(
                    channel_df,
                    x='Channel',
                    y='Predicted Engagement %',
                    color='Persona',
                    barmode='group',
                    color_discrete_sequence=['#000000', '#666666', '#CCCCCC']
                )
                
                fig_engagement.update_layout(
                    title={
                        'text': "PREDICTED ENGAGEMENT RATES BY CHANNEL AND PERSONA",
                        'font': {'size': 14, 'family': 'Inter, sans-serif', 'color': '#000000'}
                    },
                    font=dict(family="Inter, sans-serif", size=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    height=400,
                    xaxis=dict(tickangle=-45),
                    yaxis=dict(gridcolor='#E5E5E5', gridwidth=1, title='Engagement Rate (%)'),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.3,
                        xanchor="center",
                        x=0.5
                    ),
                    margin=dict(l=40, r=40, t=60, b=100)
                )
                
                st.plotly_chart(fig_engagement, use_container_width=True)
            
        else:
            st.warning("No data available for analytics. Please generate targeting insights first.")
    
    with tab5:
        st.markdown("### STRATEGIC RECOMMENDATIONS")
        
        suggestions = data['suggestions']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### CONTENT STRATEGY")
            st.markdown("Recommended content themes for maximum engagement:")
            for theme in suggestions.get('content_themes', []):
                st.markdown(f"• {theme}")
            
            st.markdown("#### PARTNERSHIP OPPORTUNITIES")
            st.markdown("Strategic partnerships to amplify your reach:")
            for idea in suggestions.get('partnership_ideas', []):
                st.markdown(f"• {idea}")
        
        with col2:
            st.markdown("#### CAMPAIGN ANGLES")
            st.markdown("High-impact messaging angles to consider:")
            for angle in suggestions.get('campaign_angles', []):
                st.markdown(f"• {angle}")
            
            st.markdown("#### VISUAL DIRECTION")
            st.markdown("Recommended visual strategy:")
            for direction in suggestions.get('visual_directions', []):
                st.markdown(f"• {direction}")
        
        # Implementation Roadmap
        st.markdown("### IMPLEMENTATION ROADMAP")
        
        roadmap_data = {
            'Phase': ['Phase 1: Foundation', 'Phase 2: Launch', 'Phase 3: Optimize', 'Phase 4: Scale'],
            'Timeline': ['Week 1-2', 'Week 3-4', 'Week 5-6', 'Week 7+'],
            'Activities': [
                'Finalize personas, Create content assets, Set up channels',
                'Launch campaigns, Begin influencer outreach, Monitor initial metrics',
                'A/B test messages, Refine targeting, Optimize channels',
                'Scale successful campaigns, Expand to new segments, Measure ROI'
            ],
            'Deliverables': [
                'Content library, Channel setup, Team alignment',
                'Live campaigns, Partnership agreements, Analytics dashboard',
                'Optimization report, Best practices guide, Updated strategies',
                'Growth metrics, ROI analysis, Future roadmap'
            ]
        }
        roadmap_df = pd.DataFrame(roadmap_data)
        st.dataframe(roadmap_df, use_container_width=True, hide_index=True)
    
    with tab6:
        st.markdown("### EXPORT & SHARE")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### DOWNLOAD REPORTS")
            
            # Text Report
            report = generate_report(data)
            st.download_button(
                label="DOWNLOAD EXECUTIVE SUMMARY (TXT)",
                data=report,
                file_name=f"TasteTarget_Report_{data['product_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # JSON Export
            json_str = json.dumps(data, indent=2)
            st.download_button(
                label="EXPORT FULL DATA (JSON)",
                data=json_str,
                file_name=f"TasteTarget_Data_{data['product_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### SHARE WITH TEAM")
            
            email_input = st.text_input("Team member emails", placeholder="email@company.com")
            access_level = st.selectbox("Access level", ["View only", "Edit", "Admin"])
            
            if st.button("SEND INVITE", use_container_width=True):
                st.success("Invitation sent successfully!")
            
            if st.button("GENERATE SHAREABLE LINK", use_container_width=True):
                st.code("https://app.tastetarget.ai/shared/abc123xyz")
                st.info("Link expires in 7 days")
        
        with col3:
            st.markdown("#### INTEGRATIONS")
            
            st.button("EXPORT TO HUBSPOT", use_container_width=True)
            st.button("EXPORT TO SALESFORCE", use_container_width=True)
            st.button("EXPORT TO GOOGLE ADS", use_container_width=True)
            st.button("EXPORT TO META BUSINESS", use_container_width=True)

elif st.session_state.current_page == 'library':
    st.markdown("## CAMPAIGN LIBRARY")
    
    # Search and Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("Search campaigns", placeholder="Search by name, date, or segment...")
    with col2:
        filter_status = st.selectbox("Status", ["All", "Active", "Completed", "Draft"])
    with col3:
        filter_date = st.selectbox("Date Range", ["All Time", "Last 30 Days", "Last 90 Days", "This Year"])
    
    # Campaign Grid
    st.markdown("### YOUR CAMPAIGNS")
    
    # Sample campaign data
    campaigns = [
        {
            "name": "Summer Collection 2024",
            "date": "June 15, 2024",
            "segments": 3,
            "performance": "92%",
            "status": "Active"
        },
        {
            "name": "Eco-Friendly Product Launch",
            "date": "June 10, 2024",
            "segments": 4,
            "performance": "87%",
            "status": "Active"
        },
        {
            "name": "Holiday Campaign 2023",
            "date": "December 1, 2023",
            "segments": 3,
            "performance": "95%",
            "status": "Completed"
        }
    ]
    
    for campaign in campaigns:
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 1, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{campaign['name']}**")
            with col2:
                st.text(campaign['date'])
            with col3:
                st.text(f"{campaign['segments']} segments")
            with col4:
                st.text(f"{campaign['performance']} success")
            with col5:
                if campaign['status'] == "Active":
                    st.success(campaign['status'])
                else:
                    st.info(campaign['status'])
            with col6:
                st.button("VIEW", key=f"view_{campaign['name']}")
            
            st.markdown("---")

elif st.session_state.current_page == 'settings':
    st.markdown("## SETTINGS")
    
    tab1, tab2, tab3, tab4 = st.tabs(["ACCOUNT", "TEAM", "INTEGRATIONS", "BILLING"])
    
    with tab1:
        st.markdown("### ACCOUNT SETTINGS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Company Name", value=company_name)
            st.text_input("Primary Email", value="marketing@company.com")
            st.selectbox("Industry", ["Technology", "Retail", "Healthcare", "Finance", "Other"])
        
        with col2:
            st.selectbox("Company Size", ["1-10", "11-50", "51-200", "201-500", "500+"])
            st.selectbox("Time Zone", ["UTC", "EST", "CST", "PST"])
            st.selectbox("Language", ["English", "Spanish", "French", "German"])
        
        if st.button("SAVE CHANGES", type="primary"):
            st.success("Settings saved successfully!")
    
    with tab2:
        st.markdown("### TEAM MANAGEMENT")
        
        # Team members table
        team_data = {
            'Name': ['John Smith', 'Sarah Johnson', 'Mike Chen'],
            'Email': ['john@company.com', 'sarah@company.com', 'mike@company.com'],
            'Role': ['Admin', 'Editor', 'Viewer'],
            'Last Active': ['Today', 'Yesterday', '3 days ago']
        }
        team_df = pd.DataFrame(team_data)
        st.dataframe(team_df, use_container_width=True, hide_index=True)
        
        # Add team member
        with st.expander("ADD TEAM MEMBER"):
            new_email = st.text_input("Email Address")
            new_role = st.selectbox("Role", ["Admin", "Editor", "Viewer"])
            if st.button("SEND INVITATION"):
                st.success("Invitation sent!")
    
    with tab3:
        st.markdown("### CONNECTED INTEGRATIONS")
        
        integrations = [
            {"name": "HubSpot", "status": "Connected", "last_sync": "2 hours ago"},
            {"name": "Google Analytics", "status": "Connected", "last_sync": "1 hour ago"},
            {"name": "Salesforce", "status": "Not Connected", "last_sync": "-"},
            {"name": "Meta Business", "status": "Connected", "last_sync": "3 hours ago"}
        ]
        
        for integration in integrations:
            col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
            
            with col1:
                st.markdown(f"**{integration['name']}**")
            with col2:
                if integration['status'] == "Connected":
                    st.success(integration['status'])
                else:
                    st.warning(integration['status'])
            with col3:
                st.text(f"Last sync: {integration['last_sync']}")
            with col4:
                if integration['status'] == "Connected":
                    st.button("DISCONNECT", key=f"disc_{integration['name']}")
                else:
                    st.button("CONNECT", key=f"conn_{integration['name']}")
    
    with tab4:
        st.markdown("### BILLING & USAGE")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Plan", "Professional", "")
        with col2:
            st.metric("Monthly Usage", "847 / 1000", "API Calls")
        with col3:
            st.metric("Next Billing", "July 1, 2024", "$299/month")
        
        st.markdown("### USAGE HISTORY")
        
        # Usage chart
        usage_data = pd.DataFrame({
            'Month': ['January', 'February', 'March', 'April', 'May', 'June'],
            'API Calls': [650, 720, 810, 890, 920, 847]
        })
        
        fig = px.line(usage_data, x='Month', y='API Calls', 
                     title="Monthly API Usage",
                     markers=True)
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif"),
            showlegend=False
        )
        fig.update_traces(line_color='#000000')
        st.plotly_chart(fig, use_container_width=True)

# If no data is available on insights page
elif st.session_state.current_page == 'insights' and not st.session_state.generated_data:
    st.markdown("## AUDIENCE INSIGHTS")
    st.info("No insights available. Generate a new campaign to see AI-powered audience intelligence.")
    if st.button("GO TO CAMPAIGN GENERATOR", type="primary"):
        st.session_state.current_page = 'generate'
        st.rerun()

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