from requests import Response
import json.decoder


class BaseCase:
    def prepare_registration_data(
            self, firstname='Jim', total_price=300, checkin_date="2023-01-01", checkout_date="2024-01-01"
    ):
        return {
            "firstname": firstname,
            "lastname": "Brown",
            "totalprice": total_price,
            "depositpaid": True,
            "bookingdates": {
                "checkin": checkin_date,
                "checkout": checkout_date
            },
            "additionalneeds": "Breakfast"
        }

    def wrong_registration_data(
            self, total_price=300, checkin_date="2023-01-01", checkout_date="2024-01-01"
    ):
        return {
            "lastname": "Brown",
            "totalprice": total_price,
            "depositpaid": True,
            "bookingdates": {
                "checkin": checkin_date,
                "checkout": checkout_date
            },
            "additionalneeds": "Breakfast"
        }