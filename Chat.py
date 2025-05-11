import streamlit as st
from llms.llm import get_available_providers, get_available_models, get_llm_response

def show_chat():
    # Initialize chat state variables if they don't exist
    if 'chat_started' not in st.session_state:
        st.session_state.chat_started = False
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'selected_provider' not in st.session_state:
        st.session_state.selected_provider = None
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    # If chat hasn't started, show provider/model selection
    if not st.session_state.chat_started:
        available_providers = get_available_providers(st.session_state.api_keys)
        provider = st.selectbox(
            "Select AI Provider",
            available_providers,
            index=None,
            placeholder="Select an AI provider",
            label_visibility="collapsed",
            accept_new_options=False
        )

        if provider:
            models = get_available_models(provider, st.session_state.api_keys)
            model = st.selectbox(
                f"Select {provider} Model",
                models,
                index=None,
                placeholder="Select a model",
                label_visibility="collapsed"
            )

        def create_chat():
            # Hide the selection UI
            st.session_state.chat_started = True
            st.session_state.selected_provider = provider
            st.session_state.selected_model = model
            # Initialize with a system message
            st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        
        # Only show the button if provider and model are selected
        if provider and model:
            st.button("Create Chat", on_click=create_chat)
    
    # If chat has started, show the chat interface
    else:
        # Display chat header with selected model
        st.markdown(f"<h3 style='color:white; background-color:#484955; padding:10px; border-radius:10px'>{st.session_state.selected_provider} - {st.session_state.selected_model}</h3>", unsafe_allow_html=True)
        st.write("")

        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] != "system":  # Don't display system messages
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # If we're currently processing a message, show the spinner
        if st.session_state.processing:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Get response from the selected LLM
                    response = get_llm_response(
                        st.session_state.selected_provider, 
                        st.session_state.selected_model, 
                        st.session_state.messages, 
                        st.session_state.api_keys
                    )
                    # Add assistant response to history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    # Set processing to False
                    st.session_state.processing = False
                    # Force a rerun to display the new message
                    st.rerun()
                    
        # Chat input for new messages
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Set processing to True
            st.session_state.processing = True
            # Force a rerun to display the new message and start processing
            st.rerun()

def main():
    # Initialize state from secrets if available
    if 'api_keys' not in st.session_state:
        st.session_state.api_keys = {
            'openai': st.secrets.get("api_keys", {}).get("openai", ""),
            'anthropic': st.secrets.get("api_keys", {}).get("anthropic", ""),
            'google': st.secrets.get("api_keys", {}).get("google", ""),
            'mistral': st.secrets.get("api_keys", {}).get("mistral", ""),
            'deepseek': st.secrets.get("api_keys", {}).get("deepseek", ""),
            'ollama': st.secrets.get("api_keys", {}).get("ollama", "11434")
        }

    # Show the chat interface on the main page
    show_chat()
            
if __name__ == "__main__":
    main()