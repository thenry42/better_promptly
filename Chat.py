import streamlit as st
from llms.llm import get_available_providers, get_available_models, get_llm_response

def show_chat():
    # Initialize chat state variables if they don't exist
    if 'chats' not in st.session_state:
        st.session_state.chats = {}
    if 'active_chat_id' not in st.session_state:
        st.session_state.active_chat_id = None
    if 'chat_counter' not in st.session_state:
        st.session_state.chat_counter = 0
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    # Sidebar for chat management
    with st.sidebar:
        st.title("Chat Management")
        
        # Create a new chat button
        if st.button("New Chat", use_container_width=True):
            # Create a new unique chat ID
            new_chat_id = f"chat_{st.session_state.chat_counter}"
            # Initialize the new chat
            st.session_state.chats[new_chat_id] = {
                "chat_started": False,
                "messages": [],
                "selected_provider": None,
                "selected_model": None,
                "title": f"Chat {st.session_state.chat_counter + 1}"
            }
            # Set the new chat as active
            st.session_state.active_chat_id = new_chat_id
            # Increment the counter
            st.session_state.chat_counter += 1
            st.rerun()
        
        # Display existing chats
        if not st.session_state.chats:
            st.info("No chats yet. Create a new chat to get started!")
        
        # Display each chat with option to select or delete
        for chat_id, chat_data in list(st.session_state.chats.items()):
            col1, col2 = st.columns([4, 1])
            
            # Chat title and selection
            with col1:
                if st.button(chat_data["title"], key=f"select_{chat_id}", use_container_width=True):
                    st.session_state.active_chat_id = chat_id
                    st.rerun()
            
            # Delete button
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    # Remove the chat
                    del st.session_state.chats[chat_id]
                    # If this was the active chat, set active to None
                    if st.session_state.active_chat_id == chat_id:
                        st.session_state.active_chat_id = next(iter(st.session_state.chats)) if st.session_state.chats else None
                    st.rerun()
    
    # Main content area - display active chat or prompt to create one
    if st.session_state.active_chat_id is None:
        st.title("Welcome to Better Promptly")
        st.info("Create a new chat to get started!")
        return
    
    # Get the active chat data
    active_chat = st.session_state.chats[st.session_state.active_chat_id]
    
    # If chat hasn't started, show provider/model selection
    if not active_chat["chat_started"]:
        st.title("Create New Chat")
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
            active_chat["chat_started"] = True
            active_chat["selected_provider"] = provider
            active_chat["selected_model"] = model
            active_chat["messages"] = []
            active_chat["title"] = f"{provider} - {model}"
        
        # Only show the button if provider and model are selected
        if provider and model:
            st.button("Start Chat", on_click=create_chat)
    
    # If chat has started, show the chat interface
    else:
        # Display chat header with selected model
        st.markdown(f"<h3 style='color:white; background-color:#484955; padding:10px; border-radius:10px'>{active_chat['selected_provider']} - {active_chat['selected_model']}</h3>", unsafe_allow_html=True)
        st.write("")

        # Display chat messages
        for message in active_chat["messages"]:
            if message["role"] != "system":  # Don't display system messages
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # If we're currently processing a message, show the spinner
        if st.session_state.processing and st.session_state.processing_chat_id == st.session_state.active_chat_id:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Get response from the selected LLM
                    response = get_llm_response(
                        active_chat["selected_provider"], 
                        active_chat["selected_model"], 
                        active_chat["messages"], 
                        st.session_state.api_keys
                    )
                    # Add assistant response to history
                    active_chat["messages"].append({"role": "assistant", "content": response})
                    # Set processing to False
                    st.session_state.processing = False
                    # Force a rerun to display the new message
                    st.rerun()
                    
        # Chat input for new messages
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to history
            active_chat["messages"].append({"role": "user", "content": prompt})
            # Set processing to True
            st.session_state.processing = True
            st.session_state.processing_chat_id = st.session_state.active_chat_id
            # Force a rerun to display the new message and start processing
            st.rerun()

def main():
    # Initialize state from secrets if available
    if 'api_keys' not in st.session_state:
        st.session_state.api_keys = {
            'openai': st.secrets.get("api_keys", {}).get("openai", ""),
            'anthropic': st.secrets.get("api_keys", {}).get("anthropic", ""),
            'gemini': st.secrets.get("api_keys", {}).get("gemini", ""),
            'mistral': st.secrets.get("api_keys", {}).get("mistral", ""),
            'deepseek': st.secrets.get("api_keys", {}).get("deepseek", ""),
            'ollama': st.secrets.get("api_keys", {}).get("ollama", "11434")
        }

    # Set page configuration
    st.set_page_config(
        page_title="Better Promptly",
        page_icon="💬",
        layout="wide",
    )

    # Show the chat interface on the main page
    show_chat()
            
if __name__ == "__main__":
    main()