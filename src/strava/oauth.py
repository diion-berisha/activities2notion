import json
import time

import requests

# Load config
with open("config/secrets.json") as f:
    config = json.load(f)

CLIENT_ID = config["strava_client_id"]
CLIENT_SECRET = config["strava_client_secret"]
REFRESH_TOKEN = config["strava_refresh_token"]
TOKEN_URL = "https://www.strava.com/oauth/token"


class StravaOAuth:
    def __init__(self):
        self.access_token = None
        self.token_expiry = 0
        self.refresh_token = REFRESH_TOKEN

    def _save_tokens(self):
        # Save the refresh token and other configuration changes
        config["strava_refresh_token"] = self.refresh_token
        with open("config/secrets.json", "w") as f:
            json.dump(config, f)

    def refresh_access_token(self):
        response = requests.post(
            TOKEN_URL,
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
        )

        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.token_expiry = time.time() + data["expires_in"]
            self.refresh_token = data["refresh_token"]
            self._save_tokens()
        else:
            raise Exception("Failed to refresh Strava access token")

    def get_access_token(self):
        # Refresh token if needed
        if self.access_token is None or time.time() >= self.token_expiry:
            self.refresh_access_token()
        return self.access_token
