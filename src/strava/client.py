import requests
from oauth import StravaOAuth

API_BASE = "https://www.strava.com/api/v3"


class StravaClient:
    def __init__(self):
        self.oauth = StravaOAuth()

    def fetch_latest_activity(self):
        access_token = self.oauth.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"{API_BASE}/athlete/activities",
            headers=headers,
            params={"per_page": 1},
        )

        if response.status_code == 200:
            activities = response.json()
            if activities:
                latest_activity = activities[0]
                return {
                    "name": latest_activity["name"],
                    "distance": latest_activity["distance"],
                    "moving_time": latest_activity["moving_time"],
                    "elapsed_time": latest_activity["elapsed_time"],
                    "type": latest_activity["type"],
                    "start_date": latest_activity["start_date"],
                }
        else:
            raise Exception(
                f"Failed to fetch latest activity from Strava: {response.status_code}"
            )


# Usage
if __name__ == "__main__":
    client = StravaClient()
    latest_activity = client.fetch_latest_activity()
    print("Latest activity:", latest_activity)

    import json

# Load config from secrets.json
with open("config/secrets.json") as f:
    config = json.load(f)

NOTION_TOKEN = config["notion_token"]
NOTION_VERSION = "2022-06-28"
