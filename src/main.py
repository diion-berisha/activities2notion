from notion.client import NotionClient
from strava.client import StravaClient

notion_client = NotionClient()
strava_client = StravaClient()


def main():
    # Fetch the latest activity
    latest_activity = strava_client.fetch_latest_activity()

    # TODO: Implement webhook trigger
    # if check_for_new_activity(latest_activity):
    # Update Notion database
    notion_client.handle_activity_entry(latest_activity)
    # else:
    # print("No new activity found.")


if __name__ == "__main__":
    main()
