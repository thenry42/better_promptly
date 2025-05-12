import streamlit as st
import time
import concurrent.futures
from .providers.llm_ollama import check_ollama, get_available_models_ollama, ollama_chat
from .providers.llm_deepseek import check_deepseek, get_available_models_deepseek, deepseek_chat
from .providers.llm_mistral import check_mistral, get_available_models_mistral, mistral_chat
from .providers.llm_anthropic import check_anthropic, get_available_models_anthropic, anthropic_chat
from .providers.llm_openai import check_openai, get_available_models_openai, openai_chat
from .providers.llm_gemini import check_gemini, get_available_models_gemini, gemini_chat

def get_available_providers(api_keys):
    """
    Get a list of available providers with valid API keys.
    Uses parallel processing to check multiple providers simultaneously.
    """
    providers = []
    provider_checkers = [
        ("Ollama", check_ollama, api_keys["ollama"]),
        ("Deepseek", check_deepseek, api_keys["deepseek"]),
        ("Mistral", check_mistral, api_keys["mistral"]),
        ("Anthropic", check_anthropic, api_keys["anthropic"]),
        ("OpenAI", check_openai, api_keys["openai"]),
        ("Gemini", check_gemini, api_keys["gemini"])
    ]
    
    # Use ThreadPoolExecutor to check providers in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_provider = {
            executor.submit(checker, key): name 
            for name, checker, key in provider_checkers
        }
        
        for future in concurrent.futures.as_completed(future_to_provider):
            provider_name = future_to_provider[future]
            try:
                if future.result():
                    providers.append(provider_name)
            except Exception as e:
                print(f"Error checking {provider_name}: {str(e)}")
    
    return providers


def get_available_models(provider, api_keys):
    """Get available models for the specified provider."""
    try:
        if provider == "Ollama":
            return get_available_models_ollama(api_keys["ollama"])
        if provider == "Deepseek":
            return get_available_models_deepseek(api_keys["deepseek"])
        if provider == "Mistral":
            return get_available_models_mistral(api_keys["mistral"])
        if provider == "Anthropic":
            return get_available_models_anthropic(api_keys["anthropic"])
        if provider == "OpenAI":
            return get_available_models_openai(api_keys["openai"])
        if provider == "Gemini":
            return get_available_models_gemini(api_keys["gemini"])
    except Exception as e:
        print(f"Error getting models for {provider}: {str(e)}")
    return []


def get_llm_response(provider, model, messages, api_keys):
    """Get a response from the specified LLM provider and model."""
    start_time = time.time()
    
    try:
        if provider == "Ollama":
            response = ollama_chat(model, messages, api_keys["ollama"])
        elif provider == "Deepseek":
            response = deepseek_chat(model, messages, api_keys["deepseek"])
        elif provider == "Mistral":
            response = mistral_chat(model, messages, api_keys["mistral"])
        elif provider == "Anthropic":
            response = anthropic_chat(model, messages, api_keys["anthropic"])
        elif provider == "OpenAI":
            response = openai_chat(model, messages, api_keys["openai"])
        elif provider == "Gemini":
            response = gemini_chat(model, messages, api_keys["gemini"])
        else:
            return f"Error: Unknown provider {provider}"
        
        # Log response time for performance monitoring
        elapsed_time = time.time() - start_time
        print(f"{provider} ({model}) response time: {elapsed_time:.2f} seconds")
        
        return response
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(f"LLM error with {provider} ({model}): {error_message}")
        return error_message
