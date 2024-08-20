from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.routes_list import LOGIN_API
from schemas.response_schema import API_Response
from schemas.auth_schema import UserLogin, UserLoginResponse
from config.database import get_db
from services.auth_services import auth_user_services
from utils.response import create_response
from utils.message import INTERNAL_SERVER_ERROR, LOGIN_SUCCESSFUL

# Initialize the APIRouter
router = APIRouter()

@router.post(
    LOGIN_API,
    response_model=API_Response,
)
def login(
    user: UserLogin,  # The request payload containing login credentials
    db: Session = Depends(get_db)  # Dependency to get the database session
):
    """
    Endpoint to handle user login.

    - **user**: The request payload validated against `UserLogin` schema containing user credentials.
    - **db**: The database session, injected using FastAPI's `Depends` function.

    Returns:
    - An API response indicating the result of the login attempt.
    """
    try:
        # Call the service function to handle authentication logic
        login_response = auth_user_services(db, user)
        
        # Check if the authentication was successful
        if not login_response["success"]:
            return create_response(
                login_response["status_code"],
                login_response["success"],
                login_response["message"],
            )

        # Transform the authentication result into the response schema format
        user_response = UserLoginResponse.from_orm(login_response["data"])
        
        # Return a successful response with user login data
        return create_response(
            status_code=login_response["status_code"],
            success=login_response["success"],
            message=login_response["message"],
            data=user_response,
        )
    
    except HTTPException as e:
        # Handle HTTP exceptions that may occur during execution
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    
    except Exception as e:
        # Handle unexpected errors with a generic server error message
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )
