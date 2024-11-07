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
