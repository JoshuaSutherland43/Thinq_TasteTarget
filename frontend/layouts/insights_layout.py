# frontend/layouts/insights_layout.py
import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import json
from datetime import datetime
from backend.services.report_generator import ReportGenerator as generate_report

class InsightsPage:
    @staticmethod
    def render(data):
        st.markdown(f"## AUDIENCE INSIGHTS: {data['product_name'].upper()}")
    
        # Summary Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Audience Segments", len(data['personas']), "AI-identified")
        with col2:
            st.metric("Message Variations", len(data['campaign_copies']), "Personalized")
        with col3:
            total_insights = sum(len(p['cultural_interests']) for p in data['personas'])
            st.metric("Cultural Insights", total_insights, "Data points")
        with col4:
            st.metric("Time Saved", "2 weeks", "vs manual research")
        
        # Tabbed Interface
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "AUDIENCE PERSONAS", 
            "MESSAGING", 
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
                                "selection_criteria": ["Engagement rate > 3%", "Audience alignment", "Content quality", "Brand fit"],
                                "examples": ["Niche bloggers", "Local personalities", "Industry specialists", "Community leaders"]
                            },
                            "Industry experts": {
                                "follower_range": "Varies - credibility matters more than reach",
                                "benefits": ["Credibility boost", "Expert validation", "Thought leadership", "B2B influence"],
                                "campaign_types": ["Expert reviews", "Educational content", "Webinars", "White papers"],
                                "budget_range": "$1,000 - $50,000 per campaign",
                                "selection_criteria": ["Industry credentials", "Published work", "Speaking engagements", "Peer recognition"],
                                "examples": ["Industry analysts", "Published authors", "Conference speakers", "Consultants"]
                            },
                            "Lifestyle creators": {
                                "follower_range": "10K - 1M+ followers",
                                "benefits": ["Lifestyle integration", "Visual storytelling", "Aspirational content", "Cross-platform reach"],
                                "campaign_types": ["Lifestyle integration", "Brand ambassadorships", "Content series", "Event coverage"],
                                "budget_range": "$500 - $100,000 per campaign",
                                "selection_criteria": ["Aesthetic alignment", "Audience demographics", "Content consistency", "Engagement quality"],
                                "examples": ["Fashion bloggers", "Travel influencers", "Wellness advocates", "Home designers"]
                            },
                            "Thought leaders": {
                                "follower_range": "Platform leaders regardless of size",
                                "benefits": ["Authority building", "Premium positioning", "Industry influence", "Long-term value"],
                                "campaign_types": ["Podcast appearances", "Article contributions", "Speaking engagements", "Advisory roles"],
                                "budget_range": "$5,000 - $200,000 per engagement",
                                "selection_criteria": ["Industry standing", "Media presence", "Network quality", "Alignment with brand values"],
                                "examples": ["CEOs", "Founders", "Innovators", "Visionaries"]
                            }
                        }
                        
                        for inf_type in persona['influencer_types']:
                            with st.expander(f"**{inf_type.upper()}**", expanded=True):
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
                                    
                                    st.markdown("**Example Influencers:**")
                                    for example in strategy.get('examples', []):
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
            st.markdown("### ANALYTICS & INSIGHTS")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Interest Distribution
                all_interests = {}
                for persona in data['personas']:
                    for category, interests in persona['cultural_interests'].items():
                        if category not in all_interests:
                            all_interests[category] = 0
                        all_interests[category] += len(interests)
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(all_interests.keys()),
                    values=list(all_interests.values()),
                    hole=.4,
                    marker=dict(colors=['#000000', '#333333', '#666666', '#999999', '#CCCCCC'])
                )])
                fig_pie.update_layout(
                    title="Interest Category Distribution",
                    font=dict(family="Inter, sans-serif"),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    height=400
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Persona Complexity
                persona_data = []
                for persona in data['personas']:
                    score = (len(persona['psychographics']) + 
                            len(persona['preferred_channels']) + 
                            sum(len(v) for v in persona['cultural_interests'].values()))
                    persona_data.append({
                        'Persona': persona['name'],
                        'Complexity Score': score
                    })
                
                df = pd.DataFrame(persona_data)
                fig_bar = go.Figure(data=[go.Bar(
                    x=df['Persona'],
                    y=df['Complexity Score'],
                    marker=dict(color='#000000')
                )])
                fig_bar.update_layout(
                    title="Audience Segment Complexity Analysis",
                    xaxis_title="Audience Segment",
                    yaxis_title="Complexity Score",
                    font=dict(family="Inter, sans-serif"),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    height=400
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Key Metrics Table
            st.markdown("### KEY PERFORMANCE INDICATORS")
            
            kpi_data = {
                'Metric': ['Audience Reach', 'Engagement Potential', 'Channel Diversity', 'Message Personalization'],
                'Score': ['87%', '92%', '85%', '95%'],
                'Benchmark': ['75%', '80%', '70%', '85%'],
                'Status': ['Above', 'Above', 'Above', 'Above']
            }
            kpi_df = pd.DataFrame(kpi_data)
            st.dataframe(kpi_df, use_container_width=True, hide_index=True)
        
        with tab4:
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
        
        with tab5:
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
