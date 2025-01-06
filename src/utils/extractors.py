import jmespath


def jmes_path(pattern, data, default=None):
    """
    Extracts data from a JSON object using a JMESPath pattern.

    Args:
        pattern (str): The JMESPath pattern to use.
        data (dict): The JSON object to extract data from.
        default (any, optional):
        The default value to return if the pattern is not found. Defaults to None.

    Returns:
        any: The extracted data, or the default value if the pattern is not found.
    """
    result = jmespath.search(pattern, data)
    return result if result is not None else default
