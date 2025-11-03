import streamlit as st

class ExcelValidadorUI:
    def __init__(self):
        self.set_page_config()

    def set_page_config(self):
        st.set_page_config(
            page_title="Validador de Schemas Excel",
            page_icon="resources/JP Logo.png",
            layout="wide"
        )
        st.title("Validador de Schemas Excel")