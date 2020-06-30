#!/usr/bin/python
from datetime import datetime


class StockTradeDay(object):
    def __init__(self, period: datetime, open: float, high: float, low: float, close: float, volume: int):
        self.period = period
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
