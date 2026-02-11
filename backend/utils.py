import re
from dateutil import parser
from datetime import date, timedelta
import requests

def clean_date_string(date_str: str) -> str:
    '''
    Removes ordinal suffixes (st, nd, rd, th) from date strings.
    
    Args:
        date_str: A string containing a date with ordinal suffixes
        
    Returns:
        str: Cleaned date string without ordinal suffixes
    '''
    return re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

def parse_date(date_str: str) -> date:
    '''
    Parses a string into a datetime.date object regardless of format.
    Uses dateutil.parser with fuzzy matching to handle various date formats.
    
    Args:
        date_str: A string containing a date in any format
        
    Returns:
        date: A datetime.date object parsed from the input string
    '''
    try:
        clean_str = clean_date_string(date_str) # clear ordinals and white space
        dt = parser.parse(clean_str, fuzzy=True) # fuzzy removes any text that isnt date
        return dt.date()
    except ValueError as e:
        raise ValueError(f"ValueError occured as {e} in parse_date function")
    except TypeError as e:
        raise TypeError(f"TypeError occured as {e} in parse_date function")
def is_relevant_date(date_text: str, lookback_days: int = 30) -> bool:
    '''
    Checks if a date range contains dates within the lookback period.
    Supports various date range separators: " - ", " – ", " ~ ", " to ".
    
    Args:
        date_text: A string containing a date or date range
        lookback_days: Number of days to look back from today (default: 30)
        
    Returns:
        bool: True if the end date is within the lookback period, False otherwise
    '''
    today = date.today()
    cutoff_date = today - timedelta(days=lookback_days)
    print(f"The cutoff date is {cutoff_date}")
    separators = [" - ", " – ", " ~ ", " to "]
    parts = [date_text]
    for sep in separators:
        if sep in date_text:
            parts = date_text.split(sep)
            if len(parts) >= 2:
                start_date = parse_date(parts[0])
                end_date = parse_date(parts[1])
                print(f"Comparing {end_date} to {cutoff_date}...")
            else:
                start_date = parse_date(date_text)
                end_date = start_date
            
            return end_date >= cutoff_date
    

def normalize_date_range(date_text: str) -> str:
    '''
    Converts a date string or range to a standardized readable format.
    
    Args:
        date_text: A string containing a date or date range (e.g., '2025/08/02 – 2025/08/23')
        
    Returns:
        str: Normalized date string in format "Aug 02, 2025 – Aug 23, 2025"
    '''
    separators = [" – ", "-", "~", " to "]
    parts = [date_text]
    for sep in separators:
        if sep in date_text:
            parts = date_text.split(sep)
            break

    parsed_dates = []
    for part in parts:
        dt = parse_date(part)
        if dt:
            parsed_dates.append(dt.strftime("%b %d, %Y"))
    
    return " – ".join(parsed_dates) if parsed_dates else ""


def deduplication(row_data: list) -> list:
    '''
    goes through row_data, if unique add to set and append, else don't do anything.
    args:
        row_data (list): contains the messy list of datas
    returns:
        unique_list: a list clean of duplicates, every element is unique
    '''
    if not isinstance(row_data, list):
        raise TypeError(f"Expected list, got {type(row_data)} instead in deduplication")
    try:
        seen = set()
        unique_list = list()
        for items in row_data:
            tupled_item = tuple(items)
            if tupled_item not in seen:
                seen.add(tupled_item)
                unique_list.append(items)
        print("Deduplication done.")
        return unique_list
    except Exception as e:
        raise Exception(f"Exception occured as {e}")

def trimEmptyString(list_events: list) -> list:
    '''
    Args:
        list_events = list

        Gets rid of any empty string for example "['', 'ssdasdda', 'asdasdad']
    returns:
        clean_list: a list without any empty elements
    
    '''
    if not isinstance(list_events, list):
        raise TypeError(f"Expected list, got {type(list_events)} instead in trimEmptyString function")
    try:
        clean_list = []
        for index in range(len(list_events)):
            clean_event = []
            for element in range(len(list_events[index])):
                if list_events[index][element] != '':
                    clean_event.append(list_events[index][element])
            clean_list.append(clean_event)
        return clean_list
    except Exception as e:
        raise Exception(f"Problem occured as {e} in trimEmptyString")
        
    
def request_error_handling(response) -> bool:
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
        print(f"HTTP error occurred: {http_err}")
    except requests.ConnectionError as conn_err:
        print(f"Error Connecting: {conn_err}")
    except requests.Timeout as time_err:
        print(f"Timeout Error: {time_err}")
    except requests.RequestException as err:
        print(f"An unexpected error occurred: {err}")
    return False