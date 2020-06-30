from unittest import TestCase, mock, main
from exceptions import DuplicateDataInTradeDays, NoTradeDayFound, NoTradeDayFoundForToday
from datetime import datetime, timedelta, date
from core import has_trade_data_for_today, calculate_last_trade_day, is_start_of_week, filter_by_trade_date, \
    calculate_percentage_difference, compare_with_today, combined_periods
from StockTradeDay import StockTradeDay


class TestCore(TestCase):

    def test_should_return_true_when_has_today_trade_data(self):
        test_stock_a = StockTradeDay(datetime.now(), 10.0, 20.0, 5.0, 12.0, 10000)
        test_stock_b = StockTradeDay(datetime.now() - timedelta(days=2), 10.0, 20.0, 5.0, 12.0, 10000)
        stock_list = [test_stock_a, test_stock_b]
        self.assertTrue(has_trade_data_for_today(stock_list))

    def test_should_return_false_when_has_no_today_trade_data(self):
        test_stock_a = StockTradeDay(datetime.now() - timedelta(days=2), 10.0, 20.0, 5.0, 12.0, 10000)
        test_stock_b = StockTradeDay(datetime.now() - timedelta(days=2), 10.0, 20.0, 5.0, 12.0, 10000)
        stock_list = [test_stock_a, test_stock_b]
        self.assertFalse(has_trade_data_for_today(stock_list),)

    @mock.patch('core.date')
    def test_should_return_friday_date_when_start_of_the_week(self, mock_date):
        mock_date.today.return_value = datetime(2020, 5, 11)
        trade_day = calculate_last_trade_day()
        self.assertEqual(trade_day, datetime(2020, 5, 8))

    @mock.patch('core.date')
    def test_should_return_yesterday_date_when_start_of_the_week(self, mock_date):
        mock_date.today.return_value = datetime(2020, 5, 12)
        trade_day = calculate_last_trade_day()
        self.assertEqual(trade_day, datetime(2020, 5, 11))

    @mock.patch('core.date')
    def test_should_return_true_if_start_of_the_week(self, mock_date):
        mock_date.today.return_value = datetime(2020, 5, 11)
        self.assertTrue(is_start_of_week())

    @mock.patch('core.date')
    def test_should_return_false_if_not_start_of_the_week(self, mock_date):
        mock_date.today.return_value = datetime(2020, 4, 11)
        self.assertFalse(is_start_of_week())

    def test_should_raise_exception_if_duplicate_days_found(self):
        trade_date = date.today()
        test_stock_a = StockTradeDay(datetime.now(), 10.0, 20.0, 5.0, 12.0, 10000)
        test_stock_b = test_stock_a
        stock_list = []
        stock_list.extend([test_stock_a, test_stock_b])
        with self.assertRaises(DuplicateDataInTradeDays):
            filter_by_trade_date(trade_date, stock_list)

    def test_should_raise_exception_if_no_trade_day_found(self):
        trade_date = date.today()
        test_stock_a = StockTradeDay(datetime.now() - timedelta(days=1), 10.0, 20.0, 5.0, 12.0, 10000)
        stock_list = [test_stock_a]
        with self.assertRaises(NoTradeDayFound):
            filter_by_trade_date(trade_date, stock_list)

    def test_should_return_trade_day_if_same_day_in_input(self):
        trade_date = date.today()
        test_stock_a = StockTradeDay(datetime.now() - timedelta(days=1), 10.0, 20.0, 5.0, 12.0, 10000)
        test_stock_b = StockTradeDay(datetime.now(), 10.0, 20.0, 5.0, 12.0, 10000)
        stock_list = []
        stock_list.extend([test_stock_a, test_stock_b])
        self.assertEqual(filter_by_trade_date(trade_date, stock_list), test_stock_b)

    def test_should_return_0_percentage_if_equal(self):
        self.assertEqual(calculate_percentage_difference(10.0, 10.0),0)

    def test_should_return_decreased_or_increased_percentage_when_calculated(self):
        self.assertEqual(calculate_percentage_difference(7.5, 10), -25.0)
        self.assertEqual(calculate_percentage_difference(10, 5), 100.0)

    def test_should_return_decreased_or_increased_percentage_when_calculated(self):
        self.assertEqual(calculate_percentage_difference(7.5, 10), -25.0)
        self.assertEqual(calculate_percentage_difference(10, 5), 100.0)

    def test_should_return_percentage_difference_between_trade_days(self):
        test_stock_a = StockTradeDay(datetime.now(), 10.0, 20.0, 5.0, 12.0, 10000)
        test_stock_b = StockTradeDay(datetime.now() - timedelta(days=2), 20.0, 30.0, 10.0, 24.0, 10000)
        test_stock_c = StockTradeDay(datetime.now() - timedelta(days=3), 10.0, 20.0, 5.0, 12.0, 10000)
        comparing_date = date.today() - timedelta(days=3)
        stock_list = [test_stock_a, test_stock_b, test_stock_c]
        self.assertEqual(compare_with_today(stock_list, comparing_date), 0)
        comparing_date = date.today() - timedelta(days=2)
        self.assertEqual(compare_with_today(stock_list, comparing_date), 50)

    def test_should_raise_exception_if_no_today_trade_day_found(self):
        test_stock_a = StockTradeDay(datetime.now() - timedelta(days=2), 20.0, 30.0, 10.0, 24.0, 10000)
        test_stock_b = StockTradeDay(datetime.now() - timedelta(days=3), 10.0, 20.0, 5.0, 12.0, 10000)
        stock_list = [test_stock_a, test_stock_b]
        comparing_date = date.today() - timedelta(days=3)
        with self.assertRaises(NoTradeDayFoundForToday):
            compare_with_today(stock_list, comparing_date)


if __name__ == '__main__':
    main()
