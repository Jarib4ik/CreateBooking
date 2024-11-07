import requests
from lib.logger import Logger


class MyRequests():
    @staticmethod
    def get(url: str, json: dict = None,):
        return MyRequests._send(url, json, 'GET')

    @staticmethod
    def post(url: str, json: dict = None):
        return MyRequests._send(url, json, 'POST')

    @staticmethod
    def _send(url: str, json: dict, method: str):

        url = f"https://restful-booker.herokuapp.com{url}"

        if json is None:
            json = {}

        Logger.add_requests(url, json, method)

        if method == 'POST':
            response = requests.post(url, json=json)
        elif method == 'GET':
            response = requests.get(url, json=json)
        else:
            raise Exception(f'Bad HTTP method "{method}" was received')

        Logger.add_response(response)

        return response
