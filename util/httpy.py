"""Http Module"""

import requests

class Httpy:
    """Http Request Class"""
    def get(self, url):
        """Http(s) Requests"""
        req = requests.get(url)
        return req.json()
