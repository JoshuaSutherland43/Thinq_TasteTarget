# frontend/layouts/export_layout.py
import streamlit as st
import json
from datetime import datetime
from backend.services.report_generator import ReportGenerator

class ExportPage:
    @staticmethod
    def render(data):
        st.markdown('<h2 class="section-header">Export Options</h2>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### DOCUMENTS")
            report = ReportGenerator.generate_text_report(data)
            st.download_button("DOWNLOAD REPORT", data=report, file_name=f"TasteTarget_{data['product_name']}_{datetime.now():%Y%m%d}.txt")
            st.markdown('<h2 class="section-header">Export Options</h2>', unsafe_allow_html=True)
        
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
    
    