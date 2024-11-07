import requests
from helpers.logger import Logger
from data.test_data import TestData


class CustomRequests():
    @staticmethod
    def get(url: str, json: dict = None,):
        """Формирование GET запроса"""
        return CustomRequests._send(url, json, 'GET')

    @staticmethod
    def post(url: str, json: dict = None):
        """Формирование POST запроса"""
        return CustomRequests._send(url, json, 'POST')

    @staticmethod
    def _send(url: str, json: dict, method: str):
        """Отправка запроса и запись логов"""
        url = f"{TestData.test_url}{url}"

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
