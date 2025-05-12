# Better Promptly - Optimized Chat Interface for Multiple AI Models

Better Promptly is an optimized Streamlit application that provides a unified chat interface for multiple AI models and providers.

## Features

- **Multi-Provider Support**: Interact with various AI providers including OpenAI, Anthropic, Mistral, Ollama, DeepSeek, and Gemini
- **Multiple Chat Sessions**: Create and manage multiple chat sessions with different models
- **Performance Optimized**: Efficient resource usage with caching, parallel processing, and memory management
- **Responsive UI**: Clean and user-friendly interface with optimized rendering

## Performance Optimizations

The application includes several optimizations to ensure smooth operation:

- **API Response Caching**: Reduces repeated calls to LLM providers
- **Parallel Processing**: Checks provider availability simultaneously
- **Memory Management**: Automatic garbage collection and memory usage tracking
- **Error Handling**: Graceful handling of API failures and timeouts
- **Message Windowing**: Limits the number of visible messages for better performance
- **Streamlit Configuration**: Optimized settings for faster rendering and responses

## Getting Started

### Prerequisites

- Python 3.8+
- API keys for the LLM providers you want to use

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

For the best performance, use the provided script:

```bash
./run.sh
```

Or run directly with Streamlit:

```bash
streamlit run Chat.py
```

### Configuration

1. Go to the "Settings" page
2. Enter your API keys for the providers you want to use
3. Save the settings

## Usage Tips for Optimal Performance

- Keep chat history reasonable in size for better performance
- For local models (Ollama), ensure your system has adequate resources
- Use the "New Chat" button to start fresh conversations
- Save API keys for faster startup in future sessions

## License

This project is licensed under the terms of the license included in the repository.

---

Made with ❤️ and optimized for performance