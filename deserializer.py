#!/usr/bin/python
import dateutil.parser
import logging
from exceptions import InvalidData
from StockTradeDay import StockTradeDay

logger = logging.getLogger(__name__)


def create_stock_trade_days(trading_json_data):
    stock_trade_days = []
    for trade_day in trading_json_data:
        # Convert JSON date strings to datetime type
        converted_interval = dateutil.parser.parse(trade_day, ignoretz=True)
        try:
            stock_trade_day = StockTradeDay(period=converted_interval,  **trading_json_data[trade_day])
            stock_trade_days.append(stock_trade_day)
        except Exception as err:
            logger.error('Could not create StockTradeDay class from JSON response: %s', err)
            raise InvalidData(err)
    return stock_trade_days
