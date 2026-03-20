"""
JSON configuration handler for Sect-Event-Handler.

This module manages reading, writing, and validating user configuration stored in
local_user.json. It handles game settings, webhook URLs, seen events tracking,
and date-based execution control.
"""

import json
from datetime import date
from pathlib import Path

JSON_FILE = Path(__file__).parent / "local_user.json"

def create_user_data(logger):
    """
    Creates initial user configuration file with default values.
    
    Args:
        logger: Logger object for logging messages
        
    Notes:
        Creates a JSON file with default structure including:
        - Game configurations (Arknights, Limbus Company, Azur Lane)
        - Empty webhook URLs
        - Empty seen events lists
        - Default lookback_days: 30
        - Current date placeholder
        
    The file is created only if it doesn't already exist.
    """
    logger.log_info("No user json detected, creating a new one.")
    local_user = {
        "Arknights": {
            "webhook": "",
            "proper_name": "Arknights",
            "seen_events": []
        },
        "Limbus Company": {
            "webhook": "",
            "proper_name": "Limbus Company",
            "seen_events": []
        },
        "azur_lane": {
            "webhook": "",
            "proper_name": "Azur Lane",
            "seen_events": []
        },
        "lookback_days": 30,
        "date_today": "March, 06, 2026"
    }
    try:
        with open(JSON_FILE, "w") as json_file:
            json.dump(local_user, json_file, indent=4)
    except Exception as e:
        logger.log_error(f"Failed to create user data, error occurred as: {e}")

def get_user_data():
    """
    Reads and returns user configuration data from local JSON file.
    
    Returns:
        dict: User configuration data containing:
            - Game configurations (Arknights, Limbus Company, azur_lane)
            - lookback_days: Number of days to look back for events
            - date_today: Last execution date
            
    Raises:
        FileNotFoundError: If JSON file doesn't exist (should be created first)
        json.JSONDecodeError: If JSON file is corrupted
        
    Example:
        >>> data = get_user_data()
        >>> print(data['lookback_days'])
        30
    """
    with open(JSON_FILE, "r") as f:
        return json.load(f)

def save_to_json(data):
    """
    Saves the provided data to the local JSON file.
    
    Args:
        data: Dictionary data to be serialized and written to JSON file
        
    Notes:
        - Overwrites existing file content
        - Uses indentation (4 spaces) for readability
        - Typically called after modifying user configuration
        
    Example:
        >>> user_data = get_user_data()
        >>> user_data['lookback_days'] = 45
        >>> save_to_json(user_data)
    """
    with open(JSON_FILE, "w") as f:
                json.dump(data, f, indent=4)

def check_date(logger):
    """
    Checks if the current date matches the stored date in user data.
    
    This function prevents duplicate daily runs by tracking the last execution date.
    If the date has changed since last run, it updates the stored date and returns
    False (indicating execution should proceed). If date is the same, returns True
    (indicating execution was already done today).
    
    Args:
        logger: Log object for logging messages
        
    Returns:
        bool: True if user is up to date (already ran today), False if date was updated
        
    Raises:
        KeyError: If 'date_today' key is missing from user data
        Exception: For other unexpected errors
        
    Notes:
        - Date format: "Month, DD, YYYY" (e.g., "March, 06, 2026")
        - Updates file if date has changed
        - Used by flow() to prevent duplicate daily notifications
    """
    user_data = get_user_data()
    format_date = date.today().strftime("%B, %d, %Y")
    try:
        if user_data['date_today'] != format_date:
            user_data['date_today'] = format_date
            save_to_json(user_data)
            return False
        else:
            logger.log_info(f"User is up to date. Current date is: {user_data['date_today']}")
            return True
    except KeyError as e:
        raise KeyError(f"Could not check current date, KeyError occured as: {e} [check_date function in json_handler]")
    except Exception as e:
        raise Exception(f"An error has occured as: {e} [check_date function in json_handler]")
        
def change_lookback(logger):
    """
    Interactive function to change the lookback days setting.
    
    Prompts user for new lookback days value via console input, validates it,
    and updates the configuration if different from current value.
    
    Args:
        logger: Log object for logging messages
        
    Returns:
        int: The number of days to look back (new value or existing if invalid input)
        
    Notes:
        - Uses console input (stdin) for interaction
        - Validates input is an integer
        - Returns existing value if input is invalid
        - Updates JSON file if value changed
        - Recommended default is 30 days
    """
    user_data = get_user_data()
    today = date.today()
    format_date = today.strftime("%B, %d, %Y")
    
    print(f"Current days to look back is {user_data['lookback_days']}, input new number of days to look back (recommended is 30)")
    try:
        new_lookback = int(input())
    except ValueError as e:
        logger.log_info("Did not input an integer, returning previously saved number of days to look back.")
        return user_data['lookback_days']
    
    try:
        if new_lookback == user_data['lookback_days']:
            print("User has inputted the same amount of days to look back. Exiting...")
        else:
            user_data['lookback_days'] = new_lookback
            save_to_json(user_data)
            print(f"Program will now look back at {user_data['lookback_days']} days before {format_date}")
    except KeyError as e:
        raise KeyError(f"Could not change days to look back, KeyError occured as: {e} [change_lookback function in json handler]")
    except Exception as e:
        raise Exception(f"An error has occured as: {e} [change_lookback function in json handler]")

def change_webhook(logger, game):
    """
    Interactive function to change Discord webhook URL for a specific game.
    
    Prompts user for new webhook URL via console input, validates it starts
    with 'http', and updates the configuration if different from current value.
    
    Args:
        logger: Log object for logging messages
        game: Game name to update webhook for (e.g., "Arknights", "Limbus Company")
        
    Returns:
        str: The webhook URL (new value or existing if validation fails)
        
    Notes:
        - Uses console input (stdin) for interaction
        - Validates URL starts with 'http' (http:// or https://)
        - Returns existing value if validation fails
        - Updates JSON file if value changed
        - Webhook should be a valid Discord webhook URL
    """
    user_data = get_user_data()
    
    logger.log_info(f"Current webhook is: {user_data[f'{game}_webhook']}.\nInput a new webhook link")
    
    new_webhook = input()
    if not new_webhook.startswith("http"):
        logger.log_info("Webhook inputted did not start with a proper url, returning previously saved link...")
        return user_data['webhook']
    
    
    try:
        if new_webhook == user_data['webhook']:
            logger.log_info("User has inputted the same webhook link. Exiting...")
        else:
            user_data['webhook'] = new_webhook
            save_to_json(user_data)
            print(f"The new webhook saved is: {user_data['webhook']}")
    except KeyError as e:
        raise KeyError(f"Could not change webhook, KeyError occured as: {e} [change_webhook function in json handler]")
    except Exception as e:
        raise Exception(f"An error has occured as: {e} [change_webhook function in json handler]")