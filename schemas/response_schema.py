from pydantic import BaseModel
from typing import Any, Optional

class API_Response(BaseModel):
    """
    Schema for a standard API response.

    Attributes:
    - status_code: The HTTP status code of the response.
    - success: A boolean indicating if the request was successful.
    - message: A message providing information about the request outcome.
    - data: Optional data included in the response (e.g., payload, result).
    """
    status_code: int
    success: bool
    message: str
    data: Optional[Any] = None
