from contextlib import contextmanager
from unittest.mock import patch

from src.strava.client import StravaClient
from src.strava.oauth import StravaOAuth


class StravaClientTest:
    """
    A test helper class for mocking NotionClient methods and utilities.
    """

    def __init__(self, database_id="db123"):
        self.client = StravaClient()
        oauth = StravaOAuth()
        oauth.access_token = "mocked_token"
        oauth.token_expiry = 9999999999.0

    @staticmethod
    @contextmanager
    def mock_get_response(status_code, response_data):
        """Helper function to mock the requests.get response."""
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = status_code
            mock_get.return_value.json.return_value = response_data
            mock_get.return_value.text = "Error occurred" if status_code != 200 else ""
            yield mock_get
