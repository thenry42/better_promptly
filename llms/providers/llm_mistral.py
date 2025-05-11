import mistralai

def check_mistral(api_key):
    try:
        client = mistralai.Mistral(api_key=api_key)
        models = client.models.list()
        res = [model.id for model in models.data]
        if res is not None:
            return True
        else:
            return False
    except Exception as e:
        return False

def get_available_models_mistral(api_key):
    res = []
    try:
        client = mistralai.Mistral(api_key=api_key)
        models = client.models.list()
        res = [model.id for model in models.data]
    except Exception as e:
        return []
    return res

def mistral_chat(model, message, api_key):
    try:
        with mistralai.Mistral(api_key=api_key) as mistral:
            response = mistral.chat.complete(
                model=model,
                messages=message,
            )
            return response.choices[0].message.content
    except Exception as e:
        return "Error: " + str(e)