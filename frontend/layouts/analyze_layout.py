# frontend/layouts/analyze_layout.py
import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from builders.chart_builder import ChartBuilder

class AnalyzePage:
    @staticmethod
    def render(data):
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

        with tab2:
            st.markdown('<h2 class="section-header">Campaign Messaging</h2>', unsafe_allow_html=True)

            for i, copy in enumerate(data['campaign_copies']):
                persona_name = next((p['name'] for p in data['personas']
                                    if p['persona_id'] == copy['persona_id']), f"Persona {i+1}")

                with st.expander(f"{persona_name.upper()}", expanded=(i == 0)):
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

            col1, col2 = st.columns(2)

            with col1:
                all_interests = {}
                for persona in data['personas']:
                    for category, interests in persona['cultural_interests'].items():
                        all_interests[category] = all_interests.get(category, 0) + len(interests)

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
                persona_scores = []
                for persona in data['personas']:
                    score = (
                        len(persona['psychographics']) +
                        len(persona['preferred_channels']) +
                        sum(len(v) for v in persona['cultural_interests'].values())
                    )
                    persona_scores.append({'name': persona['name'], 'score': score})

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
