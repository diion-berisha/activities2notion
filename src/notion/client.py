import json

import requests
from oauth import NotionOAuth

# Load configuration from secrets.json
with open("config/secrets.json") as f:
    config = json.load(f)

DATABASE_ID = config["notion_database_id"]
NOTION_BASE_URL = "https://api.notion.com/v1"


class NotionClient:
    def __init__(self):
        self.oauth = NotionOAuth()
        self.database_id = DATABASE_ID

    def create_activity_entry(self, activity_data):
        url = f"{NOTION_BASE_URL}/pages"
        headers = self.oauth.get_headers()
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": activity_data["name"]}}]
                },
                "Distance (m)": {"number": activity_data["distance"]},
                "Moving Time (s)": {"number": activity_data["moving_time"]},
                "Elapsed Time (s)": {"number": activity_data["elapsed_time"]},
                "Type": {"select": {"name": activity_data["type"]}},
                "Date": {"date": {"start": activity_data["start_date"]}},
            },
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Activity added to Notion database!")
        else:
            raise Exception(
                f"Failed to add activity to Notion: {response.status_code} - {response.text}"
            )


# Usage
if __name__ == "__main__":
    notion_client = NotionClient()
    sample_activity = {
        "name": "Afternoon Ride",
        "distance": 12000,
        "moving_time": 2500,
        "elapsed_time": 3000,
        "type": "Ride",
        "start_date": "2024-11-02T14:30:00Z",
    }
    notion_client.create_activity_entry(sample_activity)
