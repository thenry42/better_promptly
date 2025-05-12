import openai

def check_deepseek(api_key):
    try:
        res = []
        client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        models = client.models.list()
        res = [model.id for model in models]
        if res is not None:
            return True
        else:
            return False
    except Exception as e:
        return False

def get_available_models_deepseek(api_key):
    res = []
    try:
        client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        models = client.models.list()
        res = [model.id for model in models]
    except Exception as e:
        return []
    return res

def deepseek_chat(model, message, api_key):
    try:
        client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model=model,
            messages=message,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error: " + str(e)
