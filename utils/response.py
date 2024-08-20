from fastapi import HTTPException
from typing import Any, Dict

def create_response(
    status_code: int, success: bool, message: str, data: Any = None
) -> Dict[str, Any]:
    """
    Create a standardized API response structure.

    Args:
        status_code (int): The HTTP status code for the response.
        success (bool): Indicates whether the request was successful or not.
        message (str): A message providing additional context or information about the response.
        data (Any, optional): The data to be included in the response. Defaults to None.

    Returns:
        Dict[str, Any]: A dictionary representing the structured API response.
    """
    return {
        "status_code": status_code,  # The HTTP status code (e.g., 200, 400, 404)
        "success": success,          # Boolean indicating the success of the operation
        "message": message,          # A descriptive message about the response
        "data": data,                # Optional data payload (could be None if not applicable)
    }
