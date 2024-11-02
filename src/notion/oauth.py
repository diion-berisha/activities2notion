import json

# Load config from secrets.json
with open("config/secrets.json") as f:
    config = json.load(f)

NOTION_TOKEN = config["notion_token"]
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
