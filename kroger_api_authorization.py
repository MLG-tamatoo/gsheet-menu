import requests
from requests.auth import HTTPBasicAuth
import json

with open("credentials.json","r") as file:
    creds = json.load(file)

def GetAuth(scope):
    url = 'https://api.kroger.com/v1/connect/oauth2/token'
    x = requests.post(url, auth=HTTPBasicAuth(creds["user"], creds["pass"]), data={'grant_type': "client_credentials", "scope":scope})
    # print(x.text)
    return x.json()["access_token"]
