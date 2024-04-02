import requests 
import os
import base64
import sys
from dotenv import load_dotenv

load_dotenv()

BASEURL = f"https://{input('Enter your company name without space : ')}.api.openvpn.com/api/beta"

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]


def fetch_token(client_id:str, client_secret:str):
    url = f"{BASEURL}/oauth/token"
    headers = {"Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"}
    response = requests.post(url, headers=headers, data={"grant_type": "client_credentials", "scope": "default"})
    if response.status_code != 200:
        print("Unable to fetch token")
        print(response.content)
        sys.exit(1)
    return response.json()["access_token"]

with open("list_of_domain_and_ip.txt", "r") as f:
    dns_records = list(map(lambda x: x.split("|"), f.readlines()))
    for record in dns_records:
        url = f"{BASEURL}/dns-records"
        response = requests.post(url,headers={"Authorization":f"Bearer {fetch_token(client_id,client_secret)}"}, json={"domain": record[0], "ipv4Addresses":[ record[1]]})
        print(response.json())