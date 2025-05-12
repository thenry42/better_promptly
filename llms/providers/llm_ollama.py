import ollama


def check_ollama(port):
    try:
        client = ollama.Client(host="http://localhost:{}".format(port))
        models = client.list()
        if models:
            return True
        else:
            return False
    except Exception as e:
        return False


def get_available_models_ollama(port):
    try:
        client = ollama.Client(host="http://localhost:{}".format(port))
        models = client.list()
        res = [model["model"] for model in models["models"]]
        return res
    except Exception as e:
        return []


def ollama_chat(model, message, port):
    try:
        client = ollama.Client(host="http://localhost:{}".format(port))
        response = client.chat(model=model, messages=message, stream=False)
        return response.message.content
    except Exception as e:
        return "Error: " + str(e)
