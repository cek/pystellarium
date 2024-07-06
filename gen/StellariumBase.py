# Stub Stellarium class to bootstrap full class
# implemenation (e.g. action method generation)
import requests
import subprocess

class Stellarium:
    def __init__(self, baseUrl='http://localhost:8090/api/'):
        self.baseUrl = baseUrl
        # Ensure base url ends in '/'
        if self.baseUrl[-1] != '/':
            self.baseUrl += '/'

    def _get(self, url):
        response = requests.get(self.baseUrl + url)
        if response.status_code == 200:
            return response.json()
        return {}

    def _post(self, cmd, name, payload):
        param = {name : str(payload) }
        return requests.post(self.baseUrl + cmd, data = param).status_code == 200

    def getActions(self):
        return self._get('stelaction/list')

    def getStatus(self):
        return self._get('main/status')

    def getProperties(self):
        return self._get('stelproperty/list')
