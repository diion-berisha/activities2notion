import os

from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_API_KEY")
NOTION_VERSION = "2022-06-28"


class NotionOAuth:
    def __init__(self):
        self.api_token = NOTION_TOKEN

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        }
