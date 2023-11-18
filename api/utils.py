from typing import Any, Dict


def validate_http_url_fields(values: Dict[str, Any]) -> Dict[str, Any]:
    """
    Used to validate the HttpUrl fields in the Pydanitc models.

    Args:
        values (Dict[str, Any]): A dictionary of values.

    Returns:
        Dict[str, Any]: A dictionary of values with the HttpUrl fields validated.
    """
    for field, value in values.items():
        if isinstance(value, list):
            # Filter out invalid URLs
            values[field] = [v for v in value if v]
    return values
