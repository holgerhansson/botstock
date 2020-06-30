from unittest import TestCase, main
from datetime import datetime
from deserializer import create_stock_trade_days
from exceptions import InvalidData


class TestCreateStockTradeDays(TestCase):
    def test_should_create_stock_trade_objects_with_expected_input(self):
        test_object_json = {'2020-05-14': {'open': 114.5700, 'high': 117.0900, 'low': 111.8100,
                                           'close': 116.9500, 'volume': 5223725}}
        test_object_list = create_stock_trade_days(test_object_json)
        test_object = test_object_list[0]
        self.assertEqual(test_object.period.date(), datetime(2020, 5, 14).date())
        self.assertEqual(test_object.open, 114.5700)
        self.assertEqual(test_object.high, 117.09)
        self.assertEqual(test_object.low, 111.81)
        self.assertEqual(test_object.close, 116.95)
        self.assertEqual(test_object.volume, 5223725)

    def test_should_raise_exception_when_invalid_data(self):
        test_object_json = {'2020-05-14': {'open': 114.5700, 'high': 117.0900, 'low': 111.8100,
                                           'close': 116.9500}}
        with self.assertRaises(InvalidData):
            create_stock_trade_days(test_object_json)


if __name__ == '__main__':
    main()