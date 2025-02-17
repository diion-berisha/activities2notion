import os

import pytest

from src.strava.client import StravaClient

from . import config

strava_client_helper = config.StravaClientTest()


# Skipping for now until input is handled
@pytest.mark.skipif(
    "GITHUB_ACTIONS" in os.environ, reason="Skipping interactive test on GitHub Actions"
)
@pytest.mark.parametrize(
    "response_status_code, response_data, expected_result, expected_exception",
    [
        pytest.param(
            200,
            [
                {
                    "id": "12345",
                    "name": "Morning Ride",
                    "moving_time": 3600,
                    "distance": 15000,
                    "elapsed_time": 4000,
                    "average_heartrate": 150,
                    "max_heartrate": 180,
                    "average_cadence": 80,
                    "sport_type": "Ride",
                    "start_date": "2025-01-01T07:00:00Z",
                }
            ],
            {
                "id": "12345",
                "name": "Morning Ride",
                "time": 3600,
                "distance": 15000,
                "elapsed_time": 4000,
                "average_heart_rate": 150,
                "max_heart_rate": 180,
                "average_cadence": 80,
                "type": "Ride",
                "start_date": "2025-01-01T07:00:00Z",
            },
            None,
            id="successful_fetch",
        ),
        pytest.param(
            200,
            [],
            None,
            None,
            id="no_activities",
        ),
        pytest.param(
            500,
            [],
            None,
            Exception,
            id="server_error",
        ),
    ],
)
def test_fetch_latest_activity(
    response_status_code, response_data, expected_result, expected_exception
):
    with strava_client_helper.mock_get_response(
        status_code=response_status_code,
        response_data=response_data,
    ):
        strava_client = StravaClient()

        if expected_exception:
            with pytest.raises(expected_exception):
                strava_client.fetch_latest_activity()
        else:
            assert strava_client.fetch_latest_activity() == expected_result
