import re
from dateutil import parser
from datetime import date, timedelta
import requests

def clean_date_string(date_str: str) -> str:
    """
    Args:
        date_str: a string containing a date

    Removes ordinal suffixes (st, nd, rd, th) to make parsing easier for standard tools.
    e.g., "February 2nd, 2026" -> "February 2, 2026"
    """
    return re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

def parse_date(date_str: str):
    """
    Args:
        date_str: a string containing a date
    Parses a string into a datetime object regardless of format.
    Returns None if parsing fails.
    """
    try:
        clean_str = clean_date_string(date_str) # clear ordinals and white space
        dt = parser.parse(clean_str, fuzzy=True) # fuzzy removes any text that isnt date
        return dt.date()
    except (ValueError, TypeError):
        return None
    
def is_relevant_date(date_text: str, lookback_days: int = 30) -> bool:
    """
    Args:
        date_str: a string containing a date
        lookback_days: number of days we wanna look back

    Checks date if it's relevant or not
    """
    today = date.today()
    cutoff_date = today - timedelta(days=lookback_days)

    separators = [" - ", " – ", " ~ ", " to "]

    for sep in separators:
        if sep in date_text:
            parts = date_text.split(sep)
            break
    start_date = None
    end_date = None

    if len(parts) >= 2:
        start_date = parse_date(parts[0])
        end_date = parse_date(parts[1])
    else:
        start_date = parse_date(date_text)
        end_date = start_date

    if end_date:
        return end_date >= cutoff_date
    if start_date:
        return True
    return False

def normalize_date_range(date_text):
    """
    Args:
        date_text: a string containing a date
    Converts a date string or range to readable format.
    e.g., '2025/08/02 – 2025/08/23' -> 'Aug 02, 2025 – Aug 23, 2025'
    """
    separators = [" – ", "-", "~", " to "]
    for sep in separators:
        if sep in date_text:
            parts = date_text.split(sep)
            break
    else:
        parts = [date_text]

    parsed_dates = []
    for part in parts:
        dt = parse_date(part)
        if dt:
            parsed_dates.append(dt.strftime("%b %d, %Y"))
    
    return " – ".join(parsed_dates) if parsed_dates else ""


def deduplication(row_data: list, logger) -> list:

    try:
        seen = set()
        unique_list = list()
        for items in row_data:
            tupled_item = tuple(items)
            if tupled_item not in seen:
                seen.add(tupled_item)
                unique_list.append(items)
        logger.log_info("Deduplication done.")
        return unique_list
    except Exception as e:
        logger.log_error(f"Problem occured as {e}")
        return None

def trimEmptyString(list_events: list, logger):
    '''
    Args:
        list_events = list['', 's', 's']

        Gets rid of any empty string
    
    '''
    try:
        clean_list = []
        for events in range(len(list_events)):
            clean_event = []
            for indices in range(len(list_events[events])):
                if list_events[events][indices] != '':
                    clean_event.append(list_events[events][indices])
            clean_list.append(clean_event)
        return clean_list
    except Exception as e:
        logger.log_error(f"Problem occured as {e} in trimEmptyString")
        return None
    
def request_error_handling(response, logger) -> bool:
    '''
    Handles HTTP request errors and returns success status.
    
    Args:
        response: A requests.Response object
        
    Returns:
        bool: True if request was successful, False if an error occurred
    '''
    try:
        response.raise_for_status()
        return True
    except requests.HTTPError as http_err:
        logger.log_error(f"HTTP error occurred: {http_err}")
    except requests.ConnectionError as conn_err:
        logger.log_error(f"Error Connecting: {conn_err}")
    except requests.Timeout as time_err:
        logger.log_error(f"Timeout Error: {time_err}")
    except requests.RequestException as err:
        logger.log_error(f"An unexpected error occurred: {err}")
    return False