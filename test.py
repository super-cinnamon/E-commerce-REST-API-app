import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "auction/2", {"owner" : "salut", "prix_achat" : 2000})

print(response.json())
