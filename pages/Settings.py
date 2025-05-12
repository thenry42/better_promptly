import streamlit as st
import toml
import os
from pathlib import Path

def show_settings():
    st.header("Settings")
    st.markdown("Configure your AI settings here.")
    
    # Create a container with a dark-friendly style
    with st.container():
        st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"] > div {
            padding: 15px;
            border-radius: 10px;
            background-color: rgba(70, 70, 70, 0.2);
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # API Key settings section
        st.subheader("API Keys")
        
        # Create text inputs with saved values
        st.session_state.api_keys['openai'] = st.text_input(
            "OpenAI API Key", 
            value=st.session_state.api_keys['openai'],
            type="password",
            key="openai_input",
            help="Enter your OpenAI API key"
        )
        
        st.session_state.api_keys['anthropic'] = st.text_input(
            "Anthropic API Key", 
            value=st.session_state.api_keys['anthropic'],
            type="password",
            key="anthropic_input",
            help="Enter your Anthropic API key"
        )
        
        st.session_state.api_keys['gemini'] = st.text_input(
            "Gemini API Key", 
            value=st.session_state.api_keys['gemini'],
            type="password",
            key="gemini_input",
            help="Enter your Gemini API key"
        )
        
        st.session_state.api_keys['mistral'] = st.text_input(
            "Mistral API Key", 
            value=st.session_state.api_keys['mistral'],
            type="password",
            key="mistral_input",
            help="Enter your Mistral API key"
        )
        
        st.session_state.api_keys['deepseek'] = st.text_input(
            "DeepSeek API Key", 
            value=st.session_state.api_keys['deepseek'],
            type="password",
            key="deepseek_input",
            help="Enter your DeepSeek API key"
        )
        
        st.session_state.api_keys['ollama'] = st.text_input(
            "Ollama Port", 
            value=st.session_state.api_keys['ollama'],
            key="ollama_input",
            help="Enter the port for your local Ollama server (default: 11434)"
        )
        
        st.write("")

        # Add save and clear buttons in a column layout with better styling
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Save API Keys", key="save_keys", use_container_width=True, type="primary"):
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
        
        # Theme settings
        st.subheader("Theme Settings")
        st.info("Dark theme is currently enabled. You can change this in the settings menu (⋮) at the top-right.")

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