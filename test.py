import requests

BASE = "http://127.0.0.1:5000/"


item = {"Name": "Pend",
        "Description": "Pend",
        "Estimation": "22900-30500",
        "Acheteur":  "NONE",
        "Prix d'achat": 0}
#response = requests.delete(BASE + "auction/1")
response = requests.post(BASE + f"auction/11",{"name":"Table vintage", "description":"Table en fer avec les têtes du Britannie", "estimation":"124000-130000","owner": "NONE", "prix_achat": 0})
print(response.json())

#response = requests.get(BASE + "auction/3")
#print(response.json())
