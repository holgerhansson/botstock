from unittest import TestCase, main
from http_request import filter_response

test_object_json = """{"Meta Data": {
    "1. Information": "Daily Prices (open, high, low, close) and Volumes",
    "2. Symbol": "IBM",
    "3. Last Refreshed": "2020-05-15",
    "4. Output Size": "Compact",
    "5. Time Zone": "US/Eastern"},
    "Time Series (Daily)": {
        "2020-05-15": {
            "1. open": "115.9300",
            "2. high": "117.3900",
            "3. low": "115.2500",
            "4. close": "116.9800",
            "5. volume": "4785773"
        }
    }
}"""


class TestHTTPRequest(TestCase):
    def test_should_return_json_objects_for_daily_time_series(self):
        function_name = 'Time Series (Daily)'
        json_objects = filter_response(test_object_json, function_name)
        self.assertEqual(json_objects, {'2020-05-15': {'open': 115.93, 'high': 117.39, 'low': 115.25, 'close': 116.98,
                                                       'volume': 4785773}})


if __name__ == '__main__':
    main()