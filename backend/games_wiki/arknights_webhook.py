import requests

def send_to_discord(data: list, webhook: str):
    """
    data: list of dicts like:
        {"Event": "Event Name", "CN": "2026-02-06",
        "Global": "2026-02-10",

        {"Event_PNG": "URL_TO_IMAGE",
        "Event_PNG_URL": "IMG_WEBSITE_URL"}}
    """
    for event in data:
        event_name = event["Event"]
        cn_date = event["CN"]
        gb_date = event["Global"]
        img_url = event.get("Event_PNG_URL", "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930")
        embed = {
            "title": event_name,
            "fields": [
                {"name": "CN Date", "value":cn_date, "inline":True},
                {"name": "Global Date", "value":gb_date, "inline":True}
            ],
        }
        if img_url:
            embed["image"] = {"url": img_url}

        payload = {"embeds": [embed]}
        response = requests.post(webhook, json=payload)
        if response.status_code != 204:
            print(f"Failed to send: {response.status_code}, {response.text}")
        else:
            print(f"Sent: {event_name}")
