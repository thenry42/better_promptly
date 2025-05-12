import streamlit as st
from llms.llm import get_available_providers, get_available_models, get_llm_response
import time
import gc
import psutil
import os

# Add caching for expensive operations
@st.cache_data(ttl=300)  # Cache available providers for 5 minutes
def cached_get_available_providers(api_keys):
    return get_available_providers(api_keys)

@st.cache_data(ttl=300)  # Cache available models for 5 minutes
def cached_get_available_models(provider, api_keys):
    return get_available_models(provider, api_keys)

def get_memory_usage():
    """Return the memory usage in MB for monitoring"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / 1024 / 1024  # Convert to MB

def clean_memory():
    """Perform garbage collection to free memory"""
    gc.collect()

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
    
    # Run garbage collection periodically
    if st.session_state.get('chat_counter', 0) % 5 == 0:
        clean_memory()
    
    # Sidebar for chat management
    with st.sidebar:
        st.title("Chat Management")
        
        # Memory usage indicator (only in development)
        if os.environ.get("STREAMLIT_DEBUG"):
            mem_usage = get_memory_usage()
            st.caption(f"Memory usage: {mem_usage:.1f} MB")
        
        # Create a new chat button
        if st.button("New Chat", use_container_width=True, type="primary"):
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
                button_color = "primary" if st.session_state.active_chat_id == chat_id else "secondary"
                if st.button(chat_data["title"], key=f"select_{chat_id}", use_container_width=True, type=button_color):
                    st.session_state.active_chat_id = chat_id
                    st.rerun()
            
            # Delete button
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}", help="Delete this chat"):
                    # Remove the chat
                    del st.session_state.chats[chat_id]
                    # If this was the active chat, set active to None
                    if st.session_state.active_chat_id == chat_id:
                        st.session_state.active_chat_id = next(iter(st.session_state.chats)) if st.session_state.chats else None
                    # Run garbage collection after deleting chats
                    clean_memory()
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
        
        # Use cached function to get available providers
        try:
            with st.spinner("Loading available providers..."):
                available_providers = cached_get_available_providers(st.session_state.api_keys)
            
            if not available_providers:
                st.error("No AI providers available. Please check your API keys in Settings.")
                return
                
            provider = st.selectbox(
                "Select AI Provider",
                available_providers,
                index=None,
                placeholder="Select an AI provider",
                label_visibility="collapsed",
                accept_new_options=False
            )

            if provider:
                # Use cached function to get available models
                with st.spinner(f"Loading {provider} models..."):
                    models = cached_get_available_models(provider, st.session_state.api_keys)
                
                if not models:
                    st.error(f"No models available for {provider}. Please check your API key.")
                    return
                    
                model = st.selectbox(
                    f"Select {provider} Model",
                    models,
                    index=None,
                    placeholder="Select a model",
                    label_visibility="collapsed"
                )
        except Exception as e:
            st.error(f"Error loading providers: {str(e)}")
            return

        def create_chat():
            # Hide the selection UI
            active_chat["chat_started"] = True
            active_chat["selected_provider"] = provider
            active_chat["selected_model"] = model
            active_chat["messages"] = []
            active_chat["title"] = f"{provider} - {model}"
        
        # Only show the button if provider and model are selected
        if provider and model:
            st.button("Start Chat", on_click=create_chat, type="primary")
    
    # If chat has started, show the chat interface
    else:
        # Display chat header with selected model - original style with dark theme compatibility
        st.markdown(f"<h3 style='color:#FAFAFA; background-color:#484955; padding:10px; border-radius:10px'>{active_chat['selected_provider']} - {active_chat['selected_model']}</h3>", unsafe_allow_html=True)
        st.write("")

        # Use container for messages to improve scrolling performance
        message_container = st.container()
        
        with message_container:
            # Limit visible messages to improve performance
            MAX_VISIBLE_MESSAGES = 20
            visible_messages = active_chat["messages"][-MAX_VISIBLE_MESSAGES:] if len(active_chat["messages"]) > MAX_VISIBLE_MESSAGES else active_chat["messages"]
            
            # Display chat messages
            for message in visible_messages:
                if message["role"] != "system":  # Don't display system messages
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

        # If we're currently processing a message, show the spinner
        if st.session_state.processing and st.session_state.processing_chat_id == st.session_state.active_chat_id:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Track response time
                        start_time = time.time()
                        
                        # Get response from the selected LLM
                        response = get_llm_response(
                            active_chat["selected_provider"], 
                            active_chat["selected_model"], 
                            active_chat["messages"], 
                            st.session_state.api_keys
                        )
                        
                        # Calculate response time
                        response_time = time.time() - start_time
                        
                        # Add assistant response to history
                        active_chat["messages"].append({"role": "assistant", "content": response})
                        
                        # Log response time (for debugging)
                        print(f"LLM response time: {response_time:.2f} seconds")
                        
                    except Exception as e:
                        # Handle errors gracefully
                        error_message = f"Error: Failed to get response from {active_chat['selected_provider']} - {active_chat['selected_model']}. {str(e)}"
                        active_chat["messages"].append({"role": "assistant", "content": error_message})
                    finally:
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

    # Set page configuration with dark theme
    st.set_page_config(
        page_title="Better Promptly",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'About': "# Better Promptly\nA streamlined chat interface for various AI models."
        }
    )

    # Apply custom dark theme CSS
    st.markdown("""
    <style>
    .stButton button {
        border-radius: 8px;
    }
    
    /* Removing the custom message container styling to revert to original appearance */
    /* Keeping only minimal styling for dark theme compatibility */
    div[data-testid="stChatMessageContent"] p {
        color: #FAFAFA;
    }
    </style>
    """, unsafe_allow_html=True)

    # Show the chat interface on the main page
    show_chat()
            
if __name__ == "__main__":
    main()