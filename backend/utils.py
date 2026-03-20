import re
from dateutil import parser
from datetime import date, timedelta
import requests

def clean_date_string(date_str: str) -> str:
    """
    Removes ordinal suffixes (st, nd, rd, th) from date strings to make parsing easier.
    
    Args:
        date_str: A string containing a date with possible ordinal suffixes
        
    Returns:
        str: Date string with ordinal suffixes removed
        
    Example:
        >>> clean_date_string("February 2nd, 2026")
        "February 2, 2026"
        >>> clean_date_string("March 3rd 2025")
        "March 3 2025"
    """
    return re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

def parse_date(date_str: str):
    """
    Parses a date string into a datetime.date object using fuzzy parsing.
    
    Args:
        date_str: A string containing a date in various formats
        
    Returns:
        datetime.date: Parsed date object, or None if parsing fails
        
    Notes:
        - Uses python-dateutil parser with fuzzy=True to handle various formats
        - Automatically cleans ordinal suffixes before parsing
        - Returns only the date portion (time is discarded)
        
    Example:
        >>> parse_date("February 2nd, 2026")
        datetime.date(2026, 2, 2)
        >>> parse_date("2025-08-15")
        datetime.date(2025, 8, 15)
    """
    try:
        clean_str = clean_date_string(date_str)  # Clear ordinals and white space
        dt = parser.parse(clean_str, fuzzy=True)  # Fuzzy removes any text that isn't date
        return dt.date()
    except (ValueError, TypeError):
        return None
    
def is_relevant_date(date_text: str, lookback_days: int = 30) -> bool:
    """
    Determines if a date or date range is relevant based on lookback period.
    
    Args:
        date_text: A string containing a date or date range
        lookback_days: Number of days to look back from today (default: 30)
        
    Returns:
        bool: True if the date is within the lookback period, False otherwise
        
    Notes:
        - Handles both single dates and date ranges (separated by " - ", " – ", " ~ ", " to ")
        - For date ranges, checks if the end date is within lookback period
        - Returns False if date parsing fails
        
    Example:
        >>> is_relevant_date("February 2, 2026", lookback_days=30)
        True  # If today is within 30 days of Feb 2, 2026
        >>> is_relevant_date("Jan 1, 2025 – Jan 15, 2025", lookback_days=30)
        False # End date is too far in the past
    """
    today = date.today()
    cutoff_date = today - timedelta(days=lookback_days)

    separators = [" - ", " – ", " ~ ", " to "]
    parts = [date_text]
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
    return False

def normalize_date_range(date_text):
    """
    Converts a date string or range to a standardized readable format.
    
    Args:
        date_text: A string containing a date or date range
        
    Returns:
        str: Normalized date string in "Mon DD, YYYY" format, or empty string if parsing fails
        
    Notes:
        - Handles multiple separators: " – ", "-", "~", " to "
        - Returns dates in "Aug 02, 2025" format
        - Returns empty string if no dates can be parsed
        
    Example:
        >>> normalize_date_range("2025/08/02 – 2025/08/23")
        "Aug 02, 2025 – Aug 23, 2025"
        >>> normalize_date_range("February 2nd, 2026")
        "Feb 02, 2026"
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
    """
    Removes duplicate rows from a list while preserving order.
    
    Args:
        row_data: List of lists where each inner list represents a row of data
        logger: Logger object for logging messages
        
    Returns:
        list: List with duplicate rows removed, or None if an error occurs
        
    Notes:
        - Uses tuple conversion for hashability in set operations
        - Preserves the original order of first occurrences
        - Logs completion or errors using the provided logger
        
    Example:
        >>> deduplication([['a', 'b'], ['c', 'd'], ['a', 'b']], logger)
        [['a', 'b'], ['c', 'd']]
    """
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
        logger.log_error(f"Problem occurred as {e}")
        return None

def trimEmptyString(list_events: list, logger):
    """
    Removes empty strings from nested lists of event data.
    
    Args:
        list_events: List of lists where each inner list contains event data strings
        logger: Logger object for error logging
        
    Returns:
        list: Cleaned list with empty strings removed from inner lists, or None if error occurs
        
    Notes:
        - Processes each inner list independently
        - Only removes empty strings (''), not whitespace-only strings
        - Preserves the structure of nested lists
        
    Example:
        >>> trimEmptyString([['a', '', 'b'], ['', 'c', '']], logger)
        [['a', 'b'], ['c']]
    """
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
        logger.log_error(f"Problem occurred as {e} in trimEmptyString")
        return None
    
def request_error_handling(response, logger) -> bool:
    """
    Handles HTTP request errors and returns success status.
    
    Args:
        response: A requests.Response object from an HTTP request
        logger: Logger object for error logging
        
    Returns:
        bool: True if request was successful (2xx status), False if any error occurred
        
    Notes:
        - Checks HTTP status codes using response.raise_for_status()
        - Logs specific error types (HTTP, Connection, Timeout, RequestException)
        - Returns False for any exception, True only for successful requests
        
    Example:
        >>> response = requests.get('https://example.com')
        >>> request_error_handling(response, logger)
        True  # If status code is 200-299
    """
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

def get_webhook(name: str, user: dict, logger: object):
    """
    Retrieves Discord webhook URL for a specific game from user configuration.
    
    Args:
        name: Game name as stored in user configuration (e.g., "Arknights", "Limbus Company")
        user: Dictionary containing user configuration data
        logger: Logger object for error logging
        
    Returns:
        str: Discord webhook URL for the specified game, or None if not found
        
    Notes:
        - Looks up game configuration by name in user dictionary
        - Returns None and logs error if game configuration or webhook is missing
        - Webhook should be a valid Discord webhook URL starting with https://
        
    Example:
        >>> user_data = {"Arknights": {"webhook": "https://discord.com/api/webhooks/..."}}
        >>> get_webhook("Arknights", user_data, logger)
        "https://discord.com/api/webhooks/..."
    """
    game_name = user.get(name, "")
    if game_name is None:
        logger.log_error(f"There is no stored {name} in the local files.")
    else:
        webhook = game_name.get("webhook", "")
        if webhook is None:
            logger.log_error("There is no stored webhook in the local files.")
        else:
            return webhook