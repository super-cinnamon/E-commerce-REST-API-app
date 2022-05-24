import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "auction/0", {})

print(response.json())

#response = requests.get(BASE + "auction/3")
#print(response.json())
