import requests
from decouple import config

BASE_URL = config("BASE_URL", default="http://127.0.0.1:5005")

headers = {'content-type': 'application-json'}


def dummy_service(comando):
    '{"answer":[{"answer_type":"image", "answer":"htto"},{"answer_type":"text", "answer":"hola"},{"answer_type":"image", "answer":"link"}]}'
    return {"answer": [{"answer_type": "text", "answer": "esta es la respuesta"}]}


def post_command(data):
    url = BASE_URL + "/command/"
    try:
        r = requests.post(url, json=data)
        print(r)
        if r.status_code == 200:
            response = r.json()
            print(response)
            return response
        else:
            return {"description": "Ha ocurrido un error inesperado", "answer": []}
    except requests.exceptions.RequestException as e:
        print(e)
        return {"description": "Ha ocurrido un error inesperado", "answer": []}


API_URL = config("API_URL", default="http://127.0.0.1:5005")


def post_caso(data):
    url = API_URL + "/api/v1/casos"
    try:
        r = requests.post(url, json=data)
        if r.status_code == 200:
            # response = r.json()
            return True
    except requests.exceptions.RequestException as e:
        return False


