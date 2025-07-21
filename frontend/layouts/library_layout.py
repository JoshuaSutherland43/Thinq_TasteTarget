# frontend/layouts/library_layout.py
import streamlit as st

class LibraryPage:
    @staticmethod
    def render():
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