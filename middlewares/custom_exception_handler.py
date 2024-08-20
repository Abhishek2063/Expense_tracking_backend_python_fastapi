from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.message import MISSING_AUTHORIZATION_TOKEN


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status_code": exc.status_code,
                "message": MISSING_AUTHORIZATION_TOKEN,
            },
        )
    return await request.app.default_exception_handler(request, exc)
