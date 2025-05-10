import streamlit as st

def show_settings():
    st.header("Settings")
    st.write("Configure your AI settings here.")
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4"])


show_settings()