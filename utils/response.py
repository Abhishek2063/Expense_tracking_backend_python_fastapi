from fastapi import HTTPException
from typing import Any, Dict


def create_response(
    status_code: int, success: bool, message: str, data: Any = None
) -> Dict[str, Any]:
    return {
        "status_code": status_code,
        "success": success,
        "message": message,
        "data": data,
    }

