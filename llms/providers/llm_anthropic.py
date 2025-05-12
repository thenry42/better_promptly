import anthropic

def check_anthropic(api_key):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        models = client.models.list()
        res = [model.id for model in models]
        if res is not None:
            return True
        else:
            return False
    except Exception as e:
        return False

def get_available_models_anthropic(api_key):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        models = client.models.list()
        return [model.id for model in models]
    except Exception as e:
        return []

def anthropic_chat(model, message, api_key):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            max_tokens=4096,
            model=model,
            messages=message,
            stream=False
        )
        return response.content[0].text
    except Exception as e:
        return "Error: " + str(e)
