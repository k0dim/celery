import time

import requests

resp = requests.post(
    "http://127.0.0.1:5000/upscale",
    files={
        "file": open("example/lama_300px.png", "rb"),
    },
)
resp_data = resp.json()
print(resp_data)

task_id = resp_data.get("task_id")
print(task_id)

while True:
    resp = requests.get(f"http://127.0.0.1:5000/tasks/")
    if resp.json()['result'] is not None:
        print(resp.json())
        break
    print(resp.json())
    time.sleep(3)

resp = requests.get(f"http://127.0.0.1:5000/processed/lama_300px.png")
print(resp.json())