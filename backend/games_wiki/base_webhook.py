import requests
from pathlib import Path
import json
from .. import json_handler

def send_to_discord(config, name, logger):
    
    user_data = json_handler.get_user_data()
    webhook = user_data.get(name, {}).get("webhook")
    if webhook.startswith("https"):
        for event in config:
            embed = {
                "title": event['name'],
                "image": {"url": event['image']},
                "fields": event['fields']
            }
            payload = {
                "embeds": [embed]}
            response = requests.post(webhook, json=payload)
            if response.status_code != 204:
                logger.log_info(f"Failed to send: {response.status_code}, {response.text}")
            else:
                logger.log_info(f"Sent: {event['name']}")
    else:
        raise ValueError("Webhook does not start with HTTPS, please input a valid Webhook URL.")