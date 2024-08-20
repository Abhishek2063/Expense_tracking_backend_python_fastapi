from pydantic import BaseModel
from typing import Any, Optional


class API_Response(BaseModel):
    status_code: int
    success: bool
    message: str
    data: Optional[Any] = None
