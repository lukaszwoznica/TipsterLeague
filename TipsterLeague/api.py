import requests

API_URL = 'http://api.football-data.org/v2'
AUTH_TOKEN = 'TOKEN'


class API:
    @staticmethod
    def getRequest(request_url):
        url = "{0}/{1}".format(API_URL, request_url)
        headers = {'X-Auth-Token': AUTH_TOKEN}
        response = requests.get(url, headers=headers)
        return response.json()
