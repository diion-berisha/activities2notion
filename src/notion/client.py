import os

import requests
from dotenv import load_dotenv

from .oauth import NotionOAuth

load_dotenv()

DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

NOTION_BASE_URL = "https://api.notion.com/v1"


class NotionClient:
    def __init__(self):
        self.headers = NotionOAuth().get_headers()
        self.database_id = DATABASE_ID

    def create_activity_entry(self, activity_data):
        url = f"{NOTION_BASE_URL}/pages"
        headers = self.headers
        sport_type = activity_data.get("type", "")

        # TODO: Add support for different sport types
        # if sport_type == "Ride":
        #     payload = self.create_ride_entry(activity_data)
        # elif sport_type == "Swim":
        #     payload = self.create_swim_entry(activity_data)
        # else:
        #     payload = self.create_run_entry(activity_data)

        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": activity_data.get("name", "")}}]
                },
                "Distance (m)": {"number": activity_data.get("distance", 0)},
                "Moving Time (s)": {"number": activity_data.get("moving_time", 0)},
                "Elapsed Time (s)": {"number": activity_data.get("elapsed_time", 0)},
                "Type": {"select": {"name": sport_type}},
                "Date": {"date": {"start": activity_data.get("start_date", "")}},
                "Private Notes": {"notes": activity_data.get("private_notes", "")},
            },
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Activity added to Notion database!")
        else:
            raise Exception(
                f"Failed to add activity to Notion: {response.status_code} - {response.text}"
            )

    # def create_ride_entry(self, activity_data):
    #     pass

    # def create_swim_entry(self, activity_data):
    #     pass

    # def create_run_entry(self, activity_data):
    #     pass


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
