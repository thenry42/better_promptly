import os
import streamlit as st
from dotenv import load_dotenv
import openai
import time

# Load environment variables
load_dotenv()

def show_chat():
    st.header("Chat")
    st.write("This is the chat interface where users can interact with the AI.")
    # Chat implementation goes here

def main():
    # Show the chat interface on the main page
    show_chat()
            
if __name__ == "__main__":
    main()