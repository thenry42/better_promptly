import streamlit as st
from .providers.llm_ollama import check_ollama, get_available_models_ollama, ollama_chat
from .providers.llm_deepseek import check_deepseek, get_available_models_deepseek, deepseek_chat
from .providers.llm_mistral import check_mistral, get_available_models_mistral, mistral_chat
from .providers.llm_anthropic import check_anthropic, get_available_models_anthropic, anthropic_chat
from .providers.llm_openai import check_openai, get_available_models_openai, openai_chat
from .providers.llm_gemini import check_gemini, get_available_models_gemini, gemini_chat

def get_available_providers(api_keys):

    providers = []

    if check_ollama(api_keys["ollama"]):
        providers.append("Ollama")
    if check_deepseek(api_keys["deepseek"]):
        providers.append("Deepseek")
    if check_mistral(api_keys["mistral"]):
        providers.append("Mistral")
    if check_anthropic(api_keys["anthropic"]):
        providers.append("Anthropic")
    if check_openai(api_keys["openai"]):
        providers.append("OpenAI")
    if check_gemini(api_keys["gemini"]):
        providers.append("Gemini")
    return providers


def get_available_models(provider, api_keys):
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
    return []


def get_llm_response(provider, model, message, api_keys):
    if provider == "Ollama":
        return ollama_chat(model, message, api_keys["ollama"])
    if provider == "Deepseek":
        return deepseek_chat(model, message, api_keys["deepseek"])
    if provider == "Mistral":
        return mistral_chat(model, message, api_keys["mistral"])
    if provider == "Anthropic":
        return anthropic_chat(model, message, api_keys["anthropic"])
    if provider == "OpenAI":
        return openai_chat(model, message, api_keys["openai"])
    if provider == "Gemini":
        return gemini_chat(model, message, api_keys["gemini"])
    return ""
