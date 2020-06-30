import requests_mock
from unittest import TestCase
from http_request import get_request


class TestAlphaVantage(TestCase):

    def test_get_daily_stock_data_from_api(self):
        test_file = open('fixtures/time_series_daily_response.json', 'r')
        test_data = test_file.read()
        test_file.close()
        with requests_mock.Mocker() as m:
            m.get('http://127.0.0.1', text=test_data)
            response = get_request('http://127.0.0.1', 'test')
            self.assertEqual(response.text, test_data)