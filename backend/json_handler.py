import json
from datetime import date
from pathlib import Path

JSON_FILE = Path(__file__).parent / "local_user.json"

def get_user_data():
    with open(JSON_FILE, "r") as f:
        return json.load(f)

def save_to_json(data):
    with open(JSON_FILE, "w") as f:
                json.dump(data, f, indent=4)

def check_date(logger):
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

def change_webhook(logger):
    user_data = get_user_data()
    
    logger.log_info(f"Current webhook is: {user_data['webhook']}.\nInput a new webhook link")
    
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