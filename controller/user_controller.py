from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.routes_list import USER_CREATE_API
from schemas.response_schema import API_Response
from schemas.user_schema import User_Create_Schema, UserResponse
from config.database import get_db
from services.user_services import create_user_services
from utils.response import create_response
from utils.message import USER_CREATION_FAILED

# Initialize the APIRouter
router = APIRouter()

@router.post(
    USER_CREATE_API,
    response_model=API_Response,
)
def create_user_controller(
    create_user: User_Create_Schema,  # The schema for user creation data
    db: Session = Depends(get_db)  # Dependency to get the database session
):
    """
    Endpoint to create a new user in the system.

    - **create_user**: The request payload containing user data. It is validated using the `User_Create_Schema`.
    - **db**: The database session, injected using the `Depends` function from FastAPI.

    Returns:
    - An API response indicating success or failure of user creation.
    """
    try:
        # Call the service function to handle user creation logic
        db_user = create_user_services(db, create_user)
        
        # Check if user creation was successful
        if not db_user["success"]:
            return create_response(
                db_user["status_code"],
                db_user["success"],
                db_user["message"],
            )

        # Transform the user data into the response schema format
        user_response = UserResponse.from_orm(db_user["data"])
        
        # Return a successful response with user data
        return create_response(
            status_code=db_user["status_code"],
            success=db_user["success"],
            message=db_user["message"],
            data=user_response,
        )
    
    except HTTPException as e:
        # Handle HTTP exceptions that may be raised during execution
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    
    except Exception as e:
        # Handle unexpected errors
        return create_response(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,
        )
