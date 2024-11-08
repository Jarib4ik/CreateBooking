import datetime
import os
from requests import Response


class Logger:
    file_name = f'logs/log_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.log'

    @classmethod
    def _write_log_to_file(cls, data: str):
        """Запись логов в файл"""
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_requests(cls, url: str, json: dict, method: str):
        """Запись запроса в логи"""

        test_name = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f'\n-----\n'
        data_to_add += f'Test: {test_name}\n'
        data_to_add += f'Time: {str(datetime.datetime.now())}\n'
        data_to_add += f'Request method: {method}\n'
        data_to_add += f'Request URL: {url}\n'
        data_to_add += f'Request data: {json}\n'
        data_to_add += '\n'

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        """Запись ответа в логи"""

        data_to_add = f'Response code: {response.status_code}\n'
        data_to_add += f'Response text: {response.text}\n'
        data_to_add += f'\n-----\n'

        cls._write_log_to_file(data_to_add)