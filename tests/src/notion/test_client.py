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
    with notion_client_helper.mock_notion_client_methods(
        NotionClient, is_activity_logged_return_value=False
    ):
        notion_client = NotionClient()
        response = notion_client.handle_activity_entry(activity_data)
        assert response == expected_output


@pytest.mark.parametrize(
    "properties, post_status_code, post_response_data, expected_exception",
    [
        pytest.param(
            {"Name": {"title": [{"text": {"content": "Test Activity"}}]}},
            200,
            {},
            None,
            id="successful_create_activity_entry",
        ),
        pytest.param(
            {"Name": {"title": [{"text": {"content": "Test Activity"}}]}},
            400,
            {},
            Exception,
            id="failed_create_activity_entry",
        ),
    ],
)
def test_create_activity_entry(
    properties, post_status_code, post_response_data, expected_exception
):
    with notion_client_helper.mock_post_response(
        status_code=post_status_code, response_data=post_response_data
    ) as mock_post:
        notion_client = NotionClient()
        notion_client.database_id = "db123"
        # notion_client.create_activity_entry(properties)

        if expected_exception:
            with pytest.raises(expected_exception):
                notion_client.create_activity_entry(properties)
        else:
            notion_client.create_activity_entry(properties)

        assert mock_post.called, "requests.post should be called"
        assert mock_post.call_args[1]["json"] == {
            "parent": {"database_id": "db123"},
            "properties": properties,
        }
