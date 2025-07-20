import streamlit as st

class FormBuilder:
    @staticmethod
    def render_product_form():
        return {
            "product_name": st.text_input("Product Name"),
            "category": st.selectbox("Category", ["Food", "Tech", "Fashion"]),
            "description": st.text_area("Description")
        }