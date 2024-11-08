import allure
import pytest
from helpers.assertions import Assertions
from data.test_data import TestData
from helpers.custom_requests import CustomRequests


@allure.parent_suite('Бронирование отеля')
@allure.suite('Проверки бронирования отеля')
@allure.sub_suite('Тест-кейсы: 1, 2, 3, 4, 5, 6, 7, 8')
class TestCreateBooking(TestData):

    @pytest.fixture
    @allure.step('Бронирование отеля с корректными данными')
    def create_booking(self):
        data = self.prepare_registration_data()

        response = CustomRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')
        Assertions.assert_data_in_response(response=response, data=data)

        booking_id = response.json()['bookingid']

        return booking_id

    @allure.title('1. Проверка успешного бронирования отеля c корректными параметрами')
    @allure.step('Успешное бронирование отеля')
    @allure.description('Отправка запроса с корректными данными, проверка брони по ID')
    @allure.testcase(name=1, url='')
    def test_1_create_booking_positive(self, create_booking):
        with allure.step('Получаем "booking id" из запроса'):
            booking_id = create_booking

        with allure.step('Отправляем запрос на проверку наличия "booking_id" в системе'):
            response = CustomRequests.get(url=f'/booking/{booking_id}')

        Assertions.assert_code_status(response=response, expected_status_code=200)

    @pytest.mark.parametrize('checkin_data', TestData.exclude_params_for_date)
    @allure.title('2. Проверки бронирования отеля c некоректными данными в дате въезда')
    @allure.step('Бронирование отеля с некорректными данными в дате заезда')
    @allure.description('Проверка отправки запросов с некорректными данными в дате въезда')
    @allure.testcase(name=2, url='')
    def test_2_create_booking_str_in_checkin_date(self, checkin_data):
        data = self.prepare_registration_data(checkin_date=checkin_data)

        with allure.step('Отправка запроса с некорректной датой'):
            response = CustomRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        """По логике ожидается 400 ошибка, но API возвращает 200"""
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.title('3. Проверка бронирования отеля cо строкой в цене')
    @allure.step('Бронирование отеля со строкой в цене')
    @allure.description('Проверка отправки запроса со строковым значением в общей цене')
    @allure.testcase(name=3, url='')
    def test_3_create_booking_str_in_price(self):
        data = self.prepare_registration_data(total_price='testStr')

        with allure.step('Отправка запроса со строкой в цене'):
            response = CustomRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        """По логике ожидается 400 ошибка, но API возвращает 200"""
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.title('4. Проверка бронирования отеля c очень длинным именем')
    @allure.step('Бронирование отеля с длинным именем')
    @allure.description('Проверка отправки запросов с именем длиной в 200 символов')
    @allure.testcase(name=4, url='')
    def test_4_create_booking_long_firstname(self):
        data = self.prepare_registration_data(firstname='a' * 200)

        with allure.step('Отправка запроса с длинным именем'):
            response = CustomRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        """В документации ограничений нет, чаще всего количество символов ограничивают"""
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.title('5. Проверка бронирования отеля c датой выезда ранее даты въезда')
    @allure.step('Бронирование с выездом ранее въезда')
    @allure.description('Проверка отправки запроса с датой выезда ранее чем дата въезда')
    @allure.testcase(name=5, url='')
    def test_5_create_booking_with_checkout_early_checkin(self):
        data = self.prepare_registration_data(checkout_date='1500-01-01')

        with allure.step('Отправка запроса с выездом ранее въезда'):
            response = CustomRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.title('6. Проверки бронирования отеля с запросом без ключа')
    @allure.step('Бронирование отеля без ключа')
    @allure.description('Проверка отправки запроса без значения и ключа')
    @allure.testcase(name=6, url='')
    def test_6_create_booking_without_firstname(self):
        data = self.prepare_wrong_registration_data()

        with allure.step('Отправка запроса без ключа'):
            response = CustomRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=500)

    @allure.title('7. Проверки бронирования отеля c числом вместо имени')
    @allure.step('Бронирование отеля с числом вместо имени')
    @allure.description('Проверка отправки запроса с числом вместо имени')
    @allure.testcase(name=7, url='')
    def test_7_create_booking_num_in_firstname(self):
        data = self.prepare_registration_data(firstname=666)

        with allure.step('Отправка запроса с числом вместо имени'):
            response = CustomRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=500)

    @allure.title('8. Проверки бронирования отеля с некорректным запросом')
    @allure.step('Бронирование отеля с некорректным запросом')
    @allure.description('Проверка отправки запроса с GET запросом вместо POST')
    @allure.testcase(name=8, url='')
    def test_8_create_booking_wrong_type_of_request(self):
        data = self.prepare_registration_data()

        with allure.step('Отправка запроса с некорректным запросом'):
            response = CustomRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
