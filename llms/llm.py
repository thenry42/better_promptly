import streamlit as st
from .providers.llm_ollama import check_ollama, get_available_models_ollama, ollama_chat


def get_available_providers(api_keys):

    providers = []

    if check_ollama(api_keys["ollama"]):
        providers.append("Ollama")

    """
    if check_deepseek():
        providers.append("Deepseek")

    if check_mistral():
        providers.append("Mistral")

    if check_openai():
        providers.append("OpenAI")

    if check_anthropic():
        providers.append("Anthropic")

    if check_gemini():
        providers.append("Gemini")
    """

    return providers


def get_available_models(provider, api_keys):
    if provider == "Ollama":
        return get_available_models_ollama(api_keys["ollama"])
    return []


def get_llm_response(provider, model, message, api_keys):
    if provider == "Ollama":
        return ollama_chat(model, message, api_keys["ollama"])
    return ""
