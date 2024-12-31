def convert_seconds(seconds):
    """
    Converts seconds to hours or minutes.

    Args:
        seconds (int): The time in seconds to convert.

    Returns:
        str: The converted time in hours or minutes.
    """
    if seconds:
        if seconds < 60:
            return f"{seconds} seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minutes"
        else:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            return (
                f"{hours} hours, {remaining_minutes} minutes"
                if remaining_minutes
                else f"{hours} hours"
            )
    return None
