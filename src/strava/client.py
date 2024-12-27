import requests

from utils.extract import jmes_path

from .oauth import StravaOAuth

API_BASE = "https://www.strava.com/api/v3"


class StravaClient:
    def __init__(self):
        self.oauth = StravaOAuth()

    def fetch_latest_activity(self):
        """
        Fetches the latest activity from Strava.

        Returns:
            dict: The latest activity data.
                id (str): The activity ID.
                name (str): The activity name.
                time (int): The moving time in seconds.
                distance (int): The distance in meters.
                elapsed_time (int): The elapsed time in seconds.
                average_heart_rate (int): The average heart rate in BPM.
                max_heart_rate (int): The maximum heart rate in BPM.
                average_cadence (int): The average cadence.
                type (str): The activity type.
                start_date (str): The start date of the activity in ISO 8601 format.
        """
        access_token = self.oauth.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(
            f"{API_BASE}/athlete/activities",
            headers=headers,
            params={
                "per_page": 1,
            },
        )

        if response.status_code == 200:
            if activities := response.json():
                latest_activity = activities[0]
                return {
                    "id": jmes_path("id", latest_activity),
                    "name": jmes_path("name", latest_activity),
                    "time": jmes_path("moving_time", latest_activity),
                    "distance": jmes_path("distance", latest_activity, 0),
                    "elapsed_time": jmes_path("elapsed_time", latest_activity),
                    "average_heart_rate": jmes_path(
                        "average_heartrate", latest_activity
                    ),
                    "max_heart_rate": jmes_path("max_heartrate", latest_activity, 0),
                    "average_cadence": jmes_path("average_cadence", latest_activity, 0),
                    "type": jmes_path("sport_type", latest_activity),
                    "start_date": jmes_path("start_date", latest_activity),
                }
        else:
            raise Exception(
                f"Failed to fetch latest activity from Strava: \
                {response.status_code}, {response.text}"
            )


# Usage
if __name__ == "__main__":
    client = StravaClient()
    latest_activity = client.fetch_latest_activity()
    print("Latest activity:", latest_activity)
