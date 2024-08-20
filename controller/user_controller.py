from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from utils.routes_list import GET_ALL_USERS_LIST_WITH_PAGINATION, USER_CREATE_API
from schemas.response_schema import API_Response
from schemas.user_schema import User_Create_Schema, UserResponse
from config.database import get_db
from services.user_services import create_user_services, get_all_users_services
from utils.response import create_response
from utils.message import USER_CREATION_FAILED
from modals.users_modal import User
from middlewares.auth_middleware import authenticate_user

# Initialize the APIRouter
router = APIRouter()


@router.post(
    USER_CREATE_API,
    response_model=API_Response,
)
def create_user_controller(
    create_user: User_Create_Schema,  # The schema for user creation data
    db: Session = Depends(get_db),  # Dependency to get the database session
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


@router.get(GET_ALL_USERS_LIST_WITH_PAGINATION, response_model=API_Response)
def get_all_users_controller(
    request: Request,
    sort_by: str = "created_at",
    order: str = "asc",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),  # Ensure user is authenticated
):
    if not isinstance(user, User):  # Check if the response is a dict (error)
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    # try:
    result = get_all_users_services(
        db, sort_by=sort_by, order=order, skip=skip, limit=limit
    )
    return create_response(
        status_code=result["status_code"],
        success=result["success"],
        message=result["message"],
        data=result["data"],
    )
    # except Exception as e:
    #     return create_response(
    #         status_code=500,
    #         success=False,
    #         message=USER_CREATION_FAILED,
    #     )
