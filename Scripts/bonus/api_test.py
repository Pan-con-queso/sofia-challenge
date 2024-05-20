import requests
import time

url = 'http://127.0.0.1:8080/update'

for i in range(24):

    file = {'file': open(f'chunks/chunk_{i}.csv', 'rb')}

    resp = requests.post(url=url, files=file)
    print(resp.json())

    time.sleep(1)

