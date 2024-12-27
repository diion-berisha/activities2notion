# import json

# Load config
import os
import time

import requests
from dotenv import load_dotenv, set_key

from utils.extract import jmes_path

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
TOKEN_EXPIRY = os.getenv("STRAVA_TOKEN_EXPIRY")

TOKEN_URL = "https://www.strava.com/oauth/token"


class StravaOAuth:
    def __init__(self):
        self.access_token = None
        self.token_expiry = 0
        self.refresh_token = REFRESH_TOKEN

    def _save_tokens(self):
        # Save the refresh token and other configuration changes
        set_key(".env", "STRAVA_REFRESH_TOKEN", self.refresh_token)
        set_key(".env", "STRAVA_ACCESS_TOKEN", self.access_token)
        set_key(".env", "STRAVA_TOKEN_EXPIRY", str(self.token_expiry))

    def refresh_access_token(self):
        response = requests.post(
            TOKEN_URL,
            params={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
        )

        if response.status_code == 200:
            data = response.json()
            self.access_token = jmes_path("access_token", data)
            self.token_expiry = time.time() + jmes_path("expires_in", data)
            self.refresh_token = jmes_path("refresh_token", data)
            self._save_tokens()
        else:
            raise Exception("Failed to refresh Strava access token")

    def get_access_token(self):
        # Refresh token if needed

        # TODO: Create initial token if not exists

        if ACCESS_TOKEN is None or time.time() >= float(TOKEN_EXPIRY):
            self.refresh_access_token()

        self.access_token = ACCESS_TOKEN
        return self.access_token
