import pytest

from src.notion.client import NotionClient

from .config import NotionClientTest

notion_client_helper = NotionClientTest()


@pytest.mark.parametrize(
    "activity_data, expected_exception, expected_output",
    [
        pytest.param(
            notion_client_helper.activity_data(),
            None,
            "Activity added to Notion database!",
            id="handle_activity_entry_run",
        ),
    ],
)
def test_handle_activity_entry(activity_data, expected_exception, expected_output):
    with NotionClientTest.mock_notion_client_methods(
        NotionClient, is_activity_logged_return_value=False
    ):
        notion_client = NotionClient(database_id="db123")
        response = notion_client.handle_activity_entry(activity_data)
        assert response == expected_output
