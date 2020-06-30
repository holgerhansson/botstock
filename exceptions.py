class DuplicateDataInTradeDays(Exception):
   """Raised if at least two trade days found for the same day"""
   pass


class NoTradeDayFound(Exception):
   """Raised if no trade day found from the list"""
   def __init__(self, message):
      self.message = message;


class NoTradeDayFoundForToday(Exception):
   """Raised if no trade day found from the list"""
   pass


class InvalidData(Exception):
   """Raised if input has missing or corrupt data"""
   pass