import streamlit as st
import toml
import os
from pathlib import Path

def show_settings():
    st.header("Settings")
    st.write("Configure your AI settings here.")
    
    # Create text inputs with saved values
    st.session_state.api_keys['openai'] = st.text_input(
        "OpenAI API Key", 
        value=st.session_state.api_keys['openai'],
        type="password",
        key="openai_input"
    )
    
    st.session_state.api_keys['anthropic'] = st.text_input(
        "Anthropic API Key", 
        value=st.session_state.api_keys['anthropic'],
        type="password",
        key="anthropic_input"
    )
    
    st.session_state.api_keys['gemini'] = st.text_input(
        "Gemini API Key", 
        value=st.session_state.api_keys['gemini'],
        type="password",
        key="gemini_input"
    )
    
    st.session_state.api_keys['mistral'] = st.text_input(
        "Mistral API Key", 
        value=st.session_state.api_keys['mistral'],
        type="password",
        key="mistral_input"
    )
    
    st.session_state.api_keys['deepseek'] = st.text_input(
        "DeepSeek API Key", 
        value=st.session_state.api_keys['deepseek'],
        type="password",
        key="deepseek_input"
    )
    
    st.session_state.api_keys['ollama'] = st.text_input(
        "Ollama Port", 
        value=st.session_state.api_keys['ollama'],
        key="ollama_input"
    )
    
    st.write("")

    # Add save and clear buttons in a column layout with better styling
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Save API Keys Across Sessions", key="save_keys", use_container_width=True):
            # Update secrets file (in development environment)
            update_secrets_file(st.session_state.api_keys)
            st.success("API keys saved successfully!")
    
    with col2:
        if st.button("Clear All Keys", key="clear_keys", use_container_width=True):
            for key in st.session_state.api_keys:
                st.session_state.api_keys[key] = '' if key != 'ollama' else '11434'
            update_secrets_file(st.session_state.api_keys)
            st.success("All API keys cleared!")
            st.rerun()

def update_secrets_file(api_keys):
    """Update the .streamlit/secrets.toml file with new API keys"""
    # Only do this in development, not in production
    if not os.environ.get("STREAMLIT_DEPLOYMENT"):
        secrets_dir = Path(".streamlit")
        secrets_dir.mkdir(exist_ok=True)
        
        # Read existing secrets if the file exists
        secrets_file = secrets_dir / "secrets.toml"
        if secrets_file.exists():
            secrets = toml.load(secrets_file)
        else:
            secrets = {}
        
        # Update API keys
        if "api_keys" not in secrets:
            secrets["api_keys"] = {}
        
        secrets["api_keys"]["openai"] = api_keys["openai"]
        secrets["api_keys"]["anthropic"] = api_keys["anthropic"]
        secrets["api_keys"]["gemini"] = api_keys["gemini"]
        secrets["api_keys"]["mistral"] = api_keys["mistral"]
        secrets["api_keys"]["deepseek"] = api_keys["deepseek"]
        secrets["api_keys"]["ollama"] = api_keys["ollama"]
        
        # Write back to file
        with open(secrets_file, "w") as f:
            toml.dump(secrets, f)

# Show settings page
show_settings()