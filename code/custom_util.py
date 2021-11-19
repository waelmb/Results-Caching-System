import requests
import json
import threading

def request_task(url, body, headers):
    requests.post(url, data=json.dumps(body), headers=headers)

def fire_and_forget(url, body, headers):
    threading.Thread(target=request_task, args=(url, body, headers)).start()