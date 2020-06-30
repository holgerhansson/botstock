#!/usr/bin/python
import requests
import logging
import json
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def get_request(base_url, payload):
    try:
        response = requests.get(base_url, params=payload)
        logger.info('Requesting URL: %s', response.url)
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        logger.error('HTTP error received: %s', http_err)
    except Exception as err:
        logger.error('Technical error occurred: %s', err)


def filter_response(response_text, function_name):
    # Remove line numbers from response and exclude metadata section from JSON
    cleaned_response = json.loads(response_text, object_hook=remove_line_numbers_and_adjust_types)
    cleaned_json = cleaned_response[function_name]
    return cleaned_json


# Add custom JSON decoder filter
def remove_line_numbers_and_adjust_types(dct):
    # Detect line number and replace key
    for key in list(dct):
        if str(key)[0:2] in ('1.', '2.', '3.', '4.', '5.', '6.'):
            new_key_name = str(key)[3:]
            dct[new_key_name] = dct.pop(key)
    # Adjust types of some fields
    for key in list(dct):
        if key in ('open', 'close', 'high', 'low'):
            dct[key] = float(dct[key])
        if key == 'volume':
            dct[key] = int(dct[key])
    return dct
