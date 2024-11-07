import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.suite('Проверки бронирования отеля')
class TestCreateBooking(BaseCase):
    exclude_params = [
        'sgsfdsggsdgdsg',
        '2900-01-01',
        '01-01-2020',
        '01-2020-01',
        '798978978'
    ]

    @pytest.fixture
    def create_booking(self):
        data = self.prepare_registration_data()
        response = MyRequests.post(url='/booking', json=data)
        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')
        booking_id = response.json()['bookingid']
        return booking_id

    @allure.suite('Проверка успешного бронирования отеля c корректными параметрами')
    def test_create_booking_positive(self, create_booking):
        booking_id = create_booking

        response = MyRequests.get(url=f'/booking/{booking_id}')

        Assertions.assert_code_status(response=response, expected_status_code=200)

    @pytest.mark.parametrize('checkin_data', exclude_params)
    @allure.suite('Проверки бронирования отеля c некоректными данными в дате въезда')
    def test_create_booking_str_in_checkin_date(self, checkin_data):
        data = self.prepare_registration_data(checkin_date=checkin_data)

        response = MyRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.suite('Проверки бронирования отеля cо строкой в цене')
    def test_create_booking_str_in_price(self):
        data = self.prepare_registration_data(total_price='testStr')

        response = MyRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.suite('Проверки бронирования отеля c числом вместо имени')
    def test_create_booking_num_in_firstname(self):
        data = self.prepare_registration_data(firstname=666)

        response = MyRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=400)
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.suite('Проверки бронирования отеля c GET запросом')
    def test_create_booking_wrong_type_of_request(self):
        data = self.prepare_registration_data()

        response = MyRequests.get(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.suite('Проверки бронирования отеля c именем в 200 символов')
    def test_create_booking_long_firstname(self):
        data = self.prepare_registration_data(firstname='a' * 200)

        response = MyRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.suite('Проверки бронирования отеля с запросом без имени')
    def test_create_booking_without_firstname(self):
        data = self.wrong_registration_data()

        response = MyRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')

    @allure.suite('Проверки бронирования отеля c датой выезда ранее даты въезда')
    def test_create_booking_with_checkout_early_checkin(self):
        data = self.prepare_registration_data(checkout_date='1500-01-01')

        response = MyRequests.post(url='/booking', json=data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name='bookingid')
