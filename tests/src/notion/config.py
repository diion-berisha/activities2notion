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
    def mock_post_response(status_code, response_data):
        """Helper function to mock the requests.post response."""
        mock_post = patch("requests.post")
        mock = mock_post.start()
        mock.return_value.status_code = status_code
        mock.return_value.json.return_value = response_data
        return (
            mock_post.stop
        )  # Return the stop function to stop patching after the test

    @staticmethod
    @contextmanager
    def mock_notion_client_methods(
        client_class,
        is_activity_logged_return_value=False,
        create_activity_entry_return_value="Activity added to Notion database!",
    ):
        """A context manager for mocking NotionClient methods."""
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
