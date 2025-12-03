# It's importing the libraries that we need to use in this script.
import json
import logging
import os
import re
import sys
from datetime import datetime

import pandas as pd
import requests
import rfc3339

logger = logging.getLogger(__name__)

def get_date_string(date_object):
    """
    It takes a date object and returns a string in RFC 3339 format
    
    :param date_object: A datetime object
    :return: A string in RFC 3339 format.
    """
    return rfc3339.rfc3339(date_object)

def setup_logging():
    # Configuring the logging handler.
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    fileName = get_date_string(datetime.now())+'sonarqube_exporter'
    logPath = 'logs'
    # To avoid duplicated logs.
    if (rootLogger.hasHandlers()):
        rootLogger.handlers.clear()

    try:
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)
    except (PermissionError, OSError) as e:
        print("Info: File logging disabled due to permissions: {0}. Logging to console only.".format(e))

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    log_level = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
    logging.getLogger().setLevel(getattr(logging, log_level, logging.DEBUG))

# Convert sr to json
def sr_to_json(series):
    """
    It takes a pandas series, converts it to a json object, and returns the json object
    
    :param series: the series you want to convert to json
    :return: A dictionary with the keys being the unique values in the series and the values being the
    counts of those values.
    """
    sr = pd.Series(series)
    fre = sr.value_counts()
    d = fre.to_json()
    j_data = json.loads(d)
    return j_data

def get_json(element, json_data):
    """
    If the element is in the json_data, return the value of that element, otherwise return 0
    
    :param element: The element in the JSON file that you want to extract
    :param json_data: The JSON data that we're going to be working with
    :return: The value of the key in the json_data dictionary.
    """
    logger.debug(f"Extracting '{element}' from json_data")
    if isinstance(json_data, dict) and element in json_data:
        value = json_data[element]
        logger.debug(f"Found '{element}': {str(value)[:100]}...") # Log first 100 chars
        return value
    else:
        logger.debug(f"'{element}' not found or json_data is not a dict. Returning 0.")
        return 0

def get_data(url, token):
# Getting the data from the url and converting it to JSON.
  logger.debug(f"Starting request to URL: {url}")
  session = requests.Session()
  session.auth = token, ''
  call = getattr(session, 'get')
  try:
      res = call(url)
      logger.debug(f"Response status code: {res.status_code}")
      logger.debug(f"Response content (truncated): {str(res.content)[:200]}...")
      data = json.loads(res.content)
      return data
  except Exception as e:
      logger.error(f"Error fetching data from {url}: {e}")
      return 0

def convert(string):
    """
    It takes a string, finds the number and unit, and returns the number of bytes
    
    :param string: The string to be converted
    :return: The number of bytes in the string.
    """
    logger.debug(f"Converting string: {string}")
    if isinstance(string, (int, float)):
        logger.debug(f"Input is already a number: {string}")
        return int(string)

    if not isinstance(string, str):
        logger.debug(f"Input is not a string or number: {type(string)}. Returning 0.")
        return 0

    value = re.search(r'([0-9]+)', string)
    unit = re.search(r'([A-Z]?B)', string)

    if not value:
         logger.debug("No number found in string. Returning 0.")
         return 0

    num = int(value.group())

    if not unit:
        logger.debug("No unit found in string. Assuming bytes.")
        return num

    unit = unit.group()
    if unit == 'B':
        return num
    num *= 1024

    if unit == 'KB':
        return num
    num *= 1024

    if unit == 'MB':
        return num
    num *= 1024

    if unit == 'GB':
        return num
    num *= 1024

    if unit == 'TB':
        return num

    return num
