import json
import allure
from requests import Response


class Assertions:

    @staticmethod
    @allure.step('Сравнение ожидаемого статус-кода с фактическим')
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    @allure.step('Проверяем наличие ключа в JSON ответа')
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}"

    @staticmethod
    @allure.step('Проверяем наличие переданных ключей и значений с данными в ответе')
    def assert_data_in_response(response: Response, data):
        """Проверяем наличие ключей из запроса в переданных"""
        try:
            response_as_dict = response.json()['booking']
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        with allure.step('Проверяем наличие ключей и значений из запроса в переданных данных'):
            for key in response_as_dict:
                current_key = key
                assert key in data, f"Response JSON shouldn't have key '{current_key}'."

                assert response_as_dict[key] == data[key], (
                    f"Value mismatch at '{current_key}': expected '{data[key]}', got '{response_as_dict[key]}'."
                    )
        with allure.step('Проверяем, что все ключи из запроса есть в ответе'):
            for key in data:
                current_key = key
                assert key in response_as_dict, f"Unexpected key '{current_key}' found in the actual data."

