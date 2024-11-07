import json
from requests import Response


class Assertions:

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have ket '{name}"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"Response JSON should't have key '{name}'"

    @staticmethod
    def assert_data_in_response(response: Response, data):
        try:
            response_as_dict = response.json()['booking']
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for key in response_as_dict:
            current_key = key
            assert key in data, f"Response JSON shouldn't have key '{current_key}'."

            assert response_as_dict[key] == data[key], (
                f"Value mismatch at '{current_key}': expected '{data[key]}', got '{response_as_dict[key]}'."
            )

        for key in data:
            current_key = key
            assert key in response_as_dict, f"Unexpected key '{current_key}' found in the actual data."
