from utils.coverters import convert_seconds
from utils.extractors import jmes_path


def define_properties(activity_data):
    """
    Defines the properties for a new activity entry.

    Args:
        activity_data (dict): The activity data to define the properties for.

    Returns:
        dict: The properties for the activity entry.
    """
    time = convert_seconds(jmes_path("time", activity_data))
    return {
        "Name": {"title": [{"text": {"content": jmes_path("name", activity_data)}}]},
        "Activity ID": {"number": jmes_path("id", activity_data)},
        "Distance (m)": {"number": jmes_path("distance", activity_data)},
        "Moving Time": {"rich_text": [{"text": {"content": f"{time}"}}]},
        "Average Heart Rate": {
            "number": jmes_path("average_heart_rate", activity_data, 0)
        },
        "Max Heart Rate": {"number": jmes_path("max_heart_rate", activity_data, 0)},
        "Average Cadence": {"number": jmes_path("average_cadence", activity_data, 0)},
        "Type": {"select": {"name": jmes_path("type", activity_data)}},
        "Date": {"date": {"start": jmes_path("start_date", activity_data)}},
    }
