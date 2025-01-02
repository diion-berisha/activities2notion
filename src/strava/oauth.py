# import json

# Load config
import os
import time

import requests
from dotenv import load_dotenv, set_key

from utils.extractors import jmes_path

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
TOKEN_EXPIRY = os.getenv("STRAVA_TOKEN_EXPIRY")

TOKEN_URL = "https://www.strava.com/oauth/token"


class StravaOAuth:
    def __init__(self):
        self.access_token = ACCESS_TOKEN
        self.token_expiry = float(TOKEN_EXPIRY) if TOKEN_EXPIRY else 0
        self.refresh_token = REFRESH_TOKEN

    def _save_tokens(self):
        """
        Saves the access token, refresh token, and token expiry time to the .env file.
        """
        set_key(".env", "STRAVA_REFRESH_TOKEN", self.refresh_token)
        set_key(".env", "STRAVA_ACCESS_TOKEN", self.access_token)
        set_key(".env", "STRAVA_TOKEN_EXPIRY", str(self.token_expiry))

    def refresh_access_token(self):
        """
        Saves the new access token, refresh token, and token expiry time to the .env file.

        Raises:
            Exception: If the refresh token is not set.
        """
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
            raise Exception(f"Failed to refresh access token: {response.text}")

    def get_access_token(self):
        """
        Gets the access token.
        If the access token is not set or has expired, it will refresh the token.
        If the refresh token is not set, it will obtain an initial token.

        Returns:
            str: The access token.
        """
        if not self.access_token or time.time() >= self.token_expiry:
            if not self.refresh_token:
                self.get_initial_token()
            else:
                self.refresh_access_token()

        return self.access_token

    def get_initial_token(self):
        """
        Obtains an initial access token by redirecting the user to the Strava authorization URL.
        The user will be prompted to authorize the app and enter the code from the URL.

        Raises:
            Exception: If the authorization code is not provided.
        """
        print("Please authorize the app by visiting this URL:")
        auth_url = (
            f"https://www.strava.com/oauth/authorize?"
            f"client_id={CLIENT_ID}&redirect_uri=https://localhost/exchange_token"
            f"&response_type=code&scope=read,activity:read,activity:write"
        )
        print(auth_url)

        auth_code = input("Enter the code from the URL: ")
        response = requests.post(
            TOKEN_URL,
            params={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": auth_code,
            },
        )

        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.token_expiry = time.time() + data["expires_in"]
            self.refresh_token = data["refresh_token"]
            self._save_tokens()
        else:
            raise Exception(f"Failed to obtain initial token: {response.text}")
