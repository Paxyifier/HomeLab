import requests
import typing
import base64
from abc import ABC, abstractmethod
base64.b64encode(b"some string")
class OpenVPNServer():
    def __init__(self, company_name:str):
        self.company_name = company_name
    def get_base_url(self):
        return f"https://{self.company_name}.api.openvpn.com/api/beta"

class Credentials(ABC):
    @abstractmethod
    def get_tokens(self):
        pass



class OpenVPNCredentials(Credentials):
    def __init__(self, openvpn_server, client_id:str, client_secret:str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.openvpn_server = openvpn_server
        self.__get_token()
    def __get_token(self):
        url = self.openvpn_server.get_base_url() + "/oauth/token"
        response = requests.post(url, headers=self.__get_headers(), data={"grant_type": "client_credentials", "scope": "default"})
        self
    def __get_headers(self):
        return {"Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}"}
    def get_token(self):
        return self.token
    
"""
HTTP Client requirements
 - has credentials and updates credentials on expiry
 - adds endpoint to base url
 - adds headers to every request
 - returns dict response
"""

class HTTPClient():
    def __init__(self, credentials:OpenVPNCredentials):
        self.credentials = credentials
        self.http_client = requests.Session()
    def get(self, endpoint:str):
        url = self.credentials.openvpn_server.get_base_url() + endpoint
        response = self.http_client.get(url, headers=self.credentials.__get_headers())
        return response.json()
    def post(self, endpoint:str, data:typing.Dict):
        url = self.credentials.openvpn_server.get_base_url() + endpoint
        response = self.http_client.post(url, headers=self.credentials.__get_headers(), json=data)
        return response.json()
    def delete(self, endpoint:str):
        url = self.credentials.openvpn_server.get_base_url() + endpoint
        response = self.http_client.delete(url, headers=self.credentials.__get_headers())
        return response.json()

class OpenVPNClient():
    def __init__(self, server:OpenVPNServer, credentials:OpenVPNCredentials):
        self.server = server
        self.credentials = credentials
        self.http_client = requests.Session()

    def get_dns_records(self):
        url = f"{self.server.get_base_url()}/dns_records"
        response = requests.get(url)
        return response.json()

    def add_dns_record(self, record):
        url = f"{self.server.get_base_url()}/dns_records"
        response = requests.post(url, json=record)
        return response.json()

    def delete_dns_record(self, record_id):
        url = f"{self.server.get_base_url()}/dns_records{record_id}"
        response = requests.delete(url)
        return response.json()
