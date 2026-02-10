import requests
from pathlib import Path
import json
from .. import json_handler

user_data = json_handler.get_user_data()

def send_to_discord(data: list):
    '''
    sends to discord webhook obviously
    Args:
        data: List of event dictionaries with structure:
            {
                "Event": str (event name),
                "CN": str (CN release date),
                "Global": str (Global release date),
                "Event_PNG_URL": str (URL to event banner image, if none sends a "NO IMAGE" image)
            }
    '''
    webhook = user_data.get("webhook")
    if webhook.startswith("https"):
        for event in data:
            event_name = event["Event"]
            cn_date = event["CN"]
            gb_date = event["Global"]
            img_url = event.get("Event_PNG_URL", "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930") # send a "no-image" png in case no image
            embed = {
                "title": event_name,
                "fields": [
                    {"name": "CN Date", "value":cn_date, "inline":True},
                    {"name": "Global Date", "value":gb_date, "inline":True}
                ],
            }
            if img_url:
                embed["image"] = {"url": img_url}

            payload = {
                "embeds": [embed]}
            response = requests.post(webhook, json=payload)
            if response.status_code != 204:
                print(f"Failed to send: {response.status_code}, {response.text}")
            else:
                print(f"Sent: {event_name}")
    else:
        raise ValueError("Webhook does not start with HTTPS, please input a valid Webhook URL.")
