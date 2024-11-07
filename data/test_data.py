class TestData:
    """Тестовый URL для запросов"""
    test_url = f'https://restful-booker.herokuapp.com'

    """Тестовые значения для параметрированной проверки даты"""
    exclude_params_for_date = [
        'sgsfdsggsdgdsg',
        '2900-01-01',
        '01-01-2020',
        '01-2020-01',
        '798978978'
    ]


    def prepare_registration_data(
            self,
            firstname='Jim', lastname='Brown', total_price=300,
            deposit_paid=True, checkin_date="2023-01-01", checkout_date="2024-01-01",
            additional_needs="Breakfast"
    ) -> dict:
        """Данные для корректного запроса с возможностью изменения в тесте"""
        return {
            "firstname": firstname,
            "lastname": lastname,
            "totalprice": total_price,
            "depositpaid": deposit_paid,
            "bookingdates": {
                "checkin": checkin_date,
                "checkout": checkout_date
            },
            "additionalneeds": additional_needs
        }

    def prepare_wrong_registration_data(self) -> dict:
        """Данные без ключа 'firstname'"""
        return {
            "lastname": "Brown",
            "totalprice": 300,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2023-01-01",
                "checkout": "2024-01-01"
            },
            "additionalneeds": "Breakfast"
        }
