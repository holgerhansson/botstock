#!/usr/bin/python
import logging
from http_request import get_request, filter_response
from deserializer import create_stock_trade_days
from email_sender import send_email
from configuration import read_configuration
from exceptions import *
from datetime import date, timedelta
from common.stock_enums import Weekday

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def core(configuration):
    base_url, function, function_name, alpha_vantage_api_key, sendgrid_api_key, stock_symbol, email_from, \
        email_to, threshold = configuration
    payload = {'function': function, 'symbol': stock_symbol, 'apikey': alpha_vantage_api_key, 'outputsize': 'compact'}
    response = get_request(base_url, payload)
    all_trade_days_json = filter_response(response.text, function_name)
    all_trade_days = create_stock_trade_days(all_trade_days_json)
    stock_difference_between_days = compare_with_today(calculate_last_trade_day(), all_trade_days)
    if reached_threshold(stock_difference_between_days, threshold):
        send_email(sendgrid_api_key)


def compare_with_today(trade_day_date, all_trade_days):
    difference = None
    if has_trade_data_for_today(all_trade_days):
        try:
            todays_trade_data = filter_by_trade_date(date.today(), all_trade_days)
            compared_trade_data = filter_by_trade_date(trade_day_date, all_trade_days)
            difference = abs(calculate_percentage_difference(todays_trade_data.close, compared_trade_data.close))
            logger.info("Most recent trade day and close value: %s, %s", todays_trade_data.period.date(),
                        todays_trade_data.close)
            logger.info("Previous trade day and close value: %s, %s", compared_trade_data.period.date(),
                        compared_trade_data.close)
            logger.info("Difference between trade days: %.1f%%", difference)
        except DuplicateDataInTradeDays:
            logger.error("Duplicate entries found for the same day: %s", combined_periods(all_trade_days))
    else:
        logger.error("No trade day found in the list with today's date: %s", combined_periods(all_trade_days))
        raise NoTradeDayFoundForToday()
    return difference


def combined_periods(trade_days):
    combined = ""
    for t in trade_days:
        combined += str(t.period.date()) + " "
    return combined


def has_trade_data_for_today(stock_trade_days):
    return any(StockTradeDay for StockTradeDay in stock_trade_days if StockTradeDay.period.date() == date.today())


def calculate_last_trade_day():
    current_date = date.today()
    if is_start_of_week():
        return current_date - timedelta(days=3)
    else:
        return current_date - timedelta(days=1)


def is_start_of_week():
    return Weekday(date.today().weekday()) is Weekday.MONDAY


def reached_threshold(difference, threshold):
    return True


def filter_by_trade_date(trade_date, trade_days):
    filtered_trade_days = [StockTradeDay for StockTradeDay in trade_days if StockTradeDay.period.date() == trade_date]
    if len(filtered_trade_days) > 1:
        raise DuplicateDataInTradeDays
    elif len(filtered_trade_days) == 0:
        raise NoTradeDayFound
    else:
        return filtered_trade_days[0]


def calculate_percentage_difference(trade_data_a, trade_data_b):
    return ((trade_data_a - trade_data_b) / trade_data_b) * 100


if __name__ == '__main__':
    core(read_configuration())

