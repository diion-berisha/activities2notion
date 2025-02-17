import os

import requests
from dotenv import load_dotenv

from utils.extractors import jmes_path
from utils.properties import define_properties

from .oauth import NotionOAuth

load_dotenv()

DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

NOTION_BASE_URL = "https://api.notion.com/v1"


class NotionClient:
    def __init__(self, database_id=None):
        self.headers = NotionOAuth().get_headers()
        self.database_id = DATABASE_ID

    def handle_activity_entry(self, activity_data):
        """
        Handles an activity entry by creating a new entry in the database.

        Args:
            activity_data (dict): The activity data to handle.

        Returns:
            dict: The response from the Notion API.
        """
        properties = define_properties(activity_data)

        if self.database_id is None:
            raise Exception("Database ID not found. Please create a database first.")

        if self.is_activity_logged(activity_data):
            print("Activity already logged.")
            return

        return self.create_activity_entry(properties)

    def create_activity_entry(self, properties):
        """
        Sends a post request to the Notion API to create a new entry in the database.

        Args:
            properties (dict): The properties to add to the entry.

        Returns:
            dict: The response from the Notion API.
        """
        url = f"{NOTION_BASE_URL}/pages"
        headers = self.headers
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("Activity added to Notion database!")
        else:
            raise Exception(
                f"Failed to add activity to Notion: {response.status_code} - {response.text}"
            )

    def is_activity_logged(self, activity_data):
        """
        Checks if an activity is already logged in the database.

        Args:
            activity_data (dict): The activity data to check.

        Returns:
            bool: True if the activity is logged, False otherwise.
        """
        url = f"{NOTION_BASE_URL}/databases/{self.database_id}/query"
        headers = self.headers
        activity_id = jmes_path("id", activity_data, 0)
        payload = {
            "filter": {"property": "Activity ID", "number": {"equals": activity_id}}
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()

            return len(data["results"]) > 0
        else:
            print(f"Error querying Notion database: {response.status_code}")
            print(response.text)
            return False


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
