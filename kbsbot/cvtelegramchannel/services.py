from requests import Session
import requests
from decouple import config

BASE_URL = config("BASE_URL")

session = Session()
session.trust_env = False
session.verify = False
session.headers["Accept"] = "application/json"
session.headers["Content-Type"] = "application/json"


def dummy_service(comando):
    '{"answer":[{"answer_type":"image", "answer":"htto"},{"answer_type":"text", "answer":"hola"},{"answer_type":"image", "answer":"link"}]}'
    return {"answer": [{"answer_type": "text", "answer": "esta es la respuesta"}]}


def get_greetings():
    url = BASE_URL + "/about/agent"
    try:
        r = session.get(url, json={})
        if r.status_code == 200:
            response = r.json()
            # print(response)
            return response
    except requests.exceptions.RequestException as e:
        print(e)


def chat_with_system(data):
    url = BASE_URL + "/chat"
    json = {}
    json.update(data)
    try:
        r = session.post(url, json=json)
        # print(">>>>> SentData ", url, json)
        if r.status_code == 200:
            response = r.json()
            # print("<<<<< ReceivedData ", response)
            return response
    except requests.exceptions.RequestException as e:
        print(e)
