import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import time

# Configure Streamlit
st.set_page_config(
    page_title="TasteTarget - AI Cultural Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0;
    }
    .sub-header {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .persona-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .copy-card {
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
    }
    .suggestion-pill {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions - DEFINED HERE BEFORE USAGE
def generate_report(data: Dict) -> str:
    """Generate a formatted text report from the campaign data"""
    report = f"""
TASTETARGET CAMPAIGN REPORT
Generated: {data['generation_timestamp']}
=====================================

PRODUCT: {data['product_name']}

PERSONAS IDENTIFIED:
"""
    
    for i, persona in enumerate(data['personas'], 1):
        report += f"""
{i}. {persona['name']}
   Description: {persona['description']}
   Key Traits: {', '.join(persona['psychographics'][:3])}
   Best Channels: {', '.join(persona['preferred_channels'])}
"""
    
    report += "\n\nCAMPAIGN COPY VARIATIONS:\n"
    
    for i, copy in enumerate(data['campaign_copies'], 1):
        persona_name = next((p['name'] for p in data['personas'] if p['persona_id'] == copy['persona_id']), f"Persona {i}")
        report += f"""
For {persona_name}:
- Tagline: {copy['tagline']}
- Social: {copy['social_caption']}
- Email Subject: {copy['email_subject']}
"""
    
    report += "\n\nSTRATEGIC RECOMMENDATIONS:\n"
    
    for category, items in data['suggestions'].items():
        report += f"\n{category.replace('_', ' ').title()}:\n"
        for item in items:
            report += f"• {item}\n"
    
    return report

# Initialize session state
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None
if 'loading' not in st.session_state:
    st.session_state.loading = False

# Backend API URL
API_URL = st.secrets.get("API_URL", "http://localhost:8000")

# Header
st.markdown('<h1 class="main-header">🎯 TasteTarget</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Cultural Intelligence for Smarter Marketing</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🚀 How It Works")
    st.markdown("""
    1. **Input** your product details
    2. **AI analyzes** cultural patterns
    3. **Get** taste-based personas
    4. **Receive** tailored copy
    5. **Export** your campaign
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Why TasteTarget?")
    st.info("""
    - 🎨 **Cultural Precision**: Target by interests, not demographics
    - ⚡ **Instant Results**: Campaigns in seconds
    - 🔒 **Privacy-First**: No personal data
    - 📈 **Data-Driven**: Powered by real taste patterns
    """)
    
    st.markdown("---")
    
    # Sample products for quick demo
    st.markdown("### 🎪 Try a Demo")
    if st.button("🟢 Eco Sneakers Demo"):
        st.session_state.demo_product = {
            "name": "EcoStride Sneakers",
            "description": "Zero-waste vegan sneakers made from recycled ocean plastic",
            "values": ["sustainability", "innovation", "style"],
            "mood": ["conscious", "modern", "bold"]
        }
    
    if st.button("☕ Artisan Coffee Demo"):
        st.session_state.demo_product = {
            "name": "Ritual Coffee Roasters",
            "description": "Single-origin, fair-trade coffee with blockchain traceability",
            "values": ["quality", "transparency", "craft"],
            "mood": ["sophisticated", "authentic", "mindful"]
        }

# Main content area
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("### 📝 Product Information")
    
    # Check if demo product is selected
    demo_data = st.session_state.get('demo_product', {})
    
    product_name = st.text_input(
        "Product Name",
        value=demo_data.get('name', ''),
        placeholder="e.g., EcoStride Vegan Sneakers"
    )
    
    product_description = st.text_area(
        "Product Description",
        value=demo_data.get('description', ''),
        placeholder="Describe your product, its features, and unique selling points...",
        height=100
    )
    
    brand_values = st.multiselect(
        "Brand Values",
        options=["sustainability", "innovation", "quality", "authenticity", "minimalism", 
                 "luxury", "accessibility", "craft", "transparency", "community"],
        default=demo_data.get('values', [])
    )
    
    target_mood = st.multiselect(
        "Target Mood/Themes",
        options=["conscious", "modern", "bold", "playful", "sophisticated", 
                 "authentic", "mindful", "adventurous", "creative", "relaxed"],
        default=demo_data.get('mood', [])
    )
    
    campaign_tone = st.select_slider(
        "Campaign Tone",
        options=["poetic", "balanced", "bold", "humorous"],
        value="balanced"
    )
    
    generate_button = st.button("🚀 Generate Campaign", type="primary", use_container_width=True)

with col2:
    if generate_button and product_name and product_description:
        st.session_state.loading = True
        
        # Prepare request data
        request_data = {
            "product_name": product_name,
            "product_description": product_description,
            "brand_values": brand_values,
            "target_mood": target_mood,
            "campaign_tone": campaign_tone
        }
        
        # Show loading animation
        with st.spinner("🧠 Analyzing cultural patterns and generating campaigns..."):
            try:
                # Make API request
                response = requests.post(
                    f"{API_URL}/api/generate-targeting",
                    json=request_data,
                    timeout=60
                )
                
                if response.status_code == 200:
                    st.session_state.generated_data = response.json()
                    st.session_state.loading = False
                    st.success("✅ Campaign generated successfully!")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    st.session_state.loading = False
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Please ensure the FastAPI server is running on port 8000.")
                st.session_state.loading = False
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.session_state.loading = False
    
    elif not product_name or not product_description:
        st.info("👈 Please fill in your product information to generate a campaign")

# Display results
if st.session_state.generated_data:
    data = st.session_state.generated_data
    
    # Metrics row
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Personas Generated", len(data['personas']))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Copy Variations", len(data['campaign_copies']))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_interests = sum(len(p['cultural_interests']) for p in data['personas'])
        st.metric("Cultural Insights", total_interests)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Time Saved", "2 weeks")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Personas", "✍️ Campaign Copy", "💡 Suggestions", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 👥 Taste-Based Customer Personas")
        
        for persona in data['personas']:
            with st.expander(f"🎭 {persona['name']}", expanded=True):
                st.markdown(f"**Description:** {persona['description']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🧠 Psychographics:**")
                    for trait in persona['psychographics']:
                        st.markdown(f"• {trait}")
                    
                    st.markdown("**📱 Preferred Channels:**")
                    for channel in persona['preferred_channels']:
                        st.markdown(f"• {channel}")
                
                with col2:
                    st.markdown("**👥 Influencer Types:**")
                    for influencer in persona['influencer_types']:
                        st.markdown(f"• {influencer}")
                    
                    st.markdown("**🎨 Cultural Interests:**")
                    for category, interests in persona['cultural_interests'].items():
                        st.markdown(f"**{category.title()}:** {', '.join(interests[:3])}")
    
    with tab2:
        st.markdown("### ✍️ Personalized Campaign Copy")
        
        for i, copy in enumerate(data['campaign_copies']):
            persona_name = next((p['name'] for p in data['personas'] if p['persona_id'] == copy['persona_id']), f"Persona {i+1}")
            
            with st.expander(f"📝 Copy for {persona_name}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🏷️ Tagline:**")
                    st.info(copy['tagline'])
                    
                    st.markdown("**📱 Social Caption:**")
                    st.text_area("", value=copy['social_caption'], height=100, key=f"social_{i}")
                    
                    st.markdown("**📧 Email Subject:**")
                    st.info(copy['email_subject'])
                
                with col2:
                    st.markdown("**📢 Ad Copy:**")
                    st.text_area("", value=copy['ad_copy'], height=100, key=f"ad_{i}")
                    
                    st.markdown("**🛍️ Product Description:**")
                    st.text_area("", value=copy['product_description'], height=100, key=f"desc_{i}")
    
    with tab3:
        st.markdown("### 💡 Strategic Suggestions")
        
        suggestions = data['suggestions']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Content Themes:**")
            for theme in suggestions.get('content_themes', []):
                st.markdown(f'<span class="suggestion-pill">{theme}</span>', unsafe_allow_html=True)
            
            st.markdown("**🤝 Partnership Ideas:**")
            for idea in suggestions.get('partnership_ideas', []):
                st.markdown(f'<span class="suggestion-pill">{idea}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📐 Campaign Angles:**")
            for angle in suggestions.get('campaign_angles', []):
                st.markdown(f'<span class="suggestion-pill">{angle}</span>', unsafe_allow_html=True)
            
            st.markdown("**🎨 Visual Directions:**")
            for direction in suggestions.get('visual_directions', []):
                st.markdown(f'<span class="suggestion-pill">{direction}</span>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📊 Audience Analytics")
        
        # Create interest distribution chart
        all_interests = {}
        for persona in data['personas']:
            for category, interests in persona['cultural_interests'].items():
                if category not in all_interests:
                    all_interests[category] = []
                all_interests[category].extend(interests)
        
        # Interest categories pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(all_interests.keys()),
            values=[len(v) for v in all_interests.values()],
            hole=.3
        )])
        fig_pie.update_layout(title="Interest Distribution by Category")
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Persona comparison
        persona_data = []
        for persona in data['personas']:
            persona_data.append({
                'Persona': persona['name'],
                'Interests': sum(len(v) for v in persona['cultural_interests'].values()),
                'Channels': len(persona['preferred_channels']),
                'Traits': len(persona['psychographics'])
            })
        
        df = pd.DataFrame(persona_data)
        fig_bar = px.bar(df, x='Persona', y=['Interests', 'Channels', 'Traits'], 
                         title="Persona Complexity Comparison")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Export section
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export as JSON
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"tastetarget_{data['product_name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Export as formatted report
        report = generate_report(data)  # NOW THIS WORKS BECAUSE FUNCTION IS DEFINED ABOVE
        st.download_button(
            label="📄 Download Report",
            data=report,
            file_name=f"tastetarget_report_{data['product_name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    
    with col3:
        # Share link (mock functionality)
        if st.button("🔗 Generate Share Link"):
            st.info("Share link: https://tastetarget.ai/campaign/abc123")
            st.balloons()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🚀 Powered by AI Cultural Intelligence | 🔒 Privacy-First Marketing | ⚡ Results in Seconds</p>
        <p style='font-size: 0.8rem;'>TasteTarget © 2024 | Built for the Qloo Hackathon</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Error handling for missing backend
if st.session_state.loading == False and generate_button and not st.session_state.generated_data:
    with st.sidebar:
        st.error("⚠️ Backend Connection Issue")
        st.markdown("""
        **Quick Fix:**
        1. Install backend dependencies:
           ```bash
           pip install -r requirements.txt
           ```
        2. Add your OpenAI API key to `.env`
        3. Start the backend:
           ```bash
           python main.py
           ```
        """)

# Clear demo data after use
if 'demo_product' in st.session_state and generate_button:
    del st.session_state.demo_product