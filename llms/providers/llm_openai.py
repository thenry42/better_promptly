import openai

def check_openai(api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        models = client.models.list()
        res = [model.id for model in models]
        if res is not None:
            return True
        else:
            return False
    except Exception as e:
        return False

def get_available_models_openai(api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        models = client.models.list()
        return [model.id for model in models]
    except Exception as e:
        return []
    
def openai_chat(model, message, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=message,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error: " + str(e)
