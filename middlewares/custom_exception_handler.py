from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.message import MISSING_AUTHORIZATION_TOKEN


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom HTTP exception handler to provide more specific error responses.

    This handler intercepts HTTP exceptions and returns custom JSON responses 
    for specific status codes, particularly 401 Unauthorized.

    Parameters:
        request (Request): The incoming request object.
        exc (HTTPException): The exception raised during request handling.

    Returns:
        JSONResponse: A JSON response tailored to the exception, 
                      with custom error messages.
    """
    # Handle 401 Unauthorized exceptions with a custom message
    if exc.status_code == 401:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status_code": exc.status_code,
                "message": MISSING_AUTHORIZATION_TOKEN,
            },
        )
    
    # For all other exceptions, use the default exception handler
    return await request.app.default_exception_handler(request, exc)
