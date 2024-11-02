from src.notion.client import update_notion_database
from src.strava.client import fetch_latest_activity
from src.trigger import check_for_new_activity


def main():
    # Fetch the latest activity
    latest_activity = fetch_latest_activity()

    # Check if there's a new activity
    if check_for_new_activity(latest_activity):
        # Update Notion database
        update_notion_database(latest_activity)
        print("New activity added to Notion!")
    else:
        print("No new activity found.")


if __name__ == "__main__":
    main()
