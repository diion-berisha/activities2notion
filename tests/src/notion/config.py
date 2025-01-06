from contextlib import contextmanager
from unittest.mock import patch

from src.notion.client import NotionClient


class NotionClientTest:
    """
    A test helper class for mocking NotionClient methods and utilities.
    """

    def __init__(self, database_id="db123"):
        self.client = NotionClient(database_id=database_id)

    @staticmethod
    @contextmanager
    def mock_post_response(status_code, response_data):
        """Helper function to mock the requests.post response."""
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = status_code
            mock_post.return_value.json.return_value = response_data
            mock_post.return_value.text = "Error occurred" if status_code != 200 else ""
            yield mock_post

    @staticmethod
    @contextmanager
    def mock_notion_client_methods(
        client_class,
        is_activity_logged_return_value=False,
        create_activity_entry_return_value="Activity added to Notion database!",
    ):
        """
        A context manager for mocking NotionClient methods and requests.post.

        Args:
            client_class (class): The NotionClient class to mock.
            is_activity_logged_return_value (bool): The return value for is_activity_logged.
            create_activity_entry_return_value (str): The return value for create_activity_entry.

        Yields:
            mock_is_logged: The mock object for is_activity_logged.
            mock_create_entry: The mock object for create_activity_entry.
        """

        with patch.object(
            client_class,
            "is_activity_logged",
            return_value=is_activity_logged_return_value,
        ) as mock_is_logged, patch.object(
            client_class,
            "create_activity_entry",
            return_value=create_activity_entry_return_value,
        ) as mock_create_entry:
            yield mock_is_logged, mock_create_entry

    def activity_data(self):
        """Returns dummy activity data."""
        return {
            "id": 1,
            "activity_type": "run",
            "activity_id": 123,
            "name": "Afternoon Run",
            "distance": 12000,
            "moving_time": 2500,
            "elapsed_time": 3000,
            "type": "run",
            "start_date": "2024-11-02T14:30:00Z",
        }
