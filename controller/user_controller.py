from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from utils.routes_list import (
    DELETE_USER_API,
    GET_ALL_USERS_LIST_WITH_PAGINATION,
    GET_USER_API,
    UPDATE_USER_DETAILS,
    UPDATE_USER_PASSWORD_DETAILS,
    USER_CREATE_API,
)
from schemas.response_schema import API_Response
from schemas.user_schema import (
    User_Create_Schema,
    User_Update_Schema,
    UserResponse,
    UserUpdatePassword,
)
from config.database import get_db
from services.user_services import (
    create_user_services,
    delete_user_by_id_services,
    get_all_users_services,
    get_user_by_id_services,
    update_user_password_services,
    update_user_services,
)
from utils.response import create_response, raise_error
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
            return raise_error(
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
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )

    except Exception as e:
        # Handle unexpected errors
        return raise_error(
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
    """
    Controller function to retrieve a paginated list of all users.

    This function handles the request to fetch a paginated list of users from the database.
    It supports sorting, ordering, and pagination parameters. The user must be authenticated
    to access this endpoint.

    Parameters:
        request (Request): The incoming HTTP request object.
        sort_by (str): The field by which to sort the results (default: "created_at").
        order (str): The order in which to sort the results, either "asc" or "desc" (default: "asc").
        skip (int): The number of records to skip for pagination (default: 0).
        limit (int): The maximum number of records to return (default: 10).
        db (Session): The database session dependency injected by FastAPI.
        user (User): The authenticated user, determined by the `authenticate_user` dependency.

    Returns:
        JSONResponse: A standardized JSON response containing the list of users or an error message.
    """

    # Check if the authentication failed (i.e., user is a dict with an error response)
    if not isinstance(user, User):
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call the service function to get the list of users based on the provided parameters
        result = get_all_users_services(
            db, sort_by=sort_by, order=order, skip=skip, limit=limit
        )
        # Return the successful response with user data
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=result["data"],
        )
    except Exception as e:
        # Handle unexpected errors and return a generic error response
        return raise_error(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,  # Consider renaming this to a more appropriate message
        )


@router.get(f"{GET_USER_API}" + "{user_id}", response_model=API_Response)
def get_user_by_id_controller(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),  # Ensure user is authenticated
):
    """
    Controller function to retrieve a specific user's details by user ID.

    This function handles the request to fetch a user's details based on their ID.
    The user must be authenticated to access this endpoint.

    Parameters:
        user_id (int): The unique identifier of the user to retrieve.
        db (Session): The database session dependency injected by FastAPI.
        user (User): The authenticated user, determined by the `authenticate_user` dependency.

    Returns:
        JSONResponse: A standardized JSON response containing the user's details or an error message.
    """

    # Check if the authentication failed (i.e., user is a dict with an error response)
    if not isinstance(user, User):
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call the service function to get the user's details by ID
        result = get_user_by_id_services(db, user_id)
        if not result["success"]:
            # Handle the case where the user is not found or another error occurs
            return raise_error(
                result["status_code"],
                result["success"],
                result["message"],
            )

        # Convert the retrieved user data into a response model
        user_response = UserResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=user_response,
        )
    except Exception as e:
        # Handle unexpected errors and return a generic error response
        return raise_error(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,  # Consider renaming this to a more appropriate message
        )


@router.put(f"{UPDATE_USER_DETAILS}" + "{user_id}", response_model=API_Response)
def update_user_details_controller(
    user_id: int,
    user_update: User_Update_Schema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Controller to update user details.

    Parameters:
    - user_id: ID of the user to be updated.
    - user_update: Schema object containing user update details.
    - db: Database session dependency.
    - user: Authenticated user object.

    Returns:
    - API response with the status of the update operation.
    """
    if not isinstance(user, User):  # Check if the authenticated user is valid
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        result = update_user_services(db, user_id, user_update)
        if not result["success"]:
            return raise_error(
                result["status_code"],
                result["success"],
                result["message"],
            )

        user_response = UserResponse.from_orm(
            result["data"]
        )  # Transform result data into response model
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=user_response,
        )
    except Exception as e:
        # Log the exception (consider adding a logger)
        return raise_error(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,
        )


@router.put(
    f"{UPDATE_USER_PASSWORD_DETAILS}" + "{user_id}", response_model=API_Response
)
def update_user_password_details_controller(
    user_id: int,
    user_update_password: UserUpdatePassword,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Controller to update user password.

    Parameters:
    - user_id: ID of the user whose password is to be updated.
    - user_update_password: Schema object containing current and new password.
    - db: Database session dependency.
    - user: Authenticated user object.

    Returns:
    - API response with the status of the password update operation.
    """
    if not isinstance(user, User):  # Check if the authenticated user is valid
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        result = update_user_password_services(db, user_id, user_update_password)
        if not result["success"]:
            return raise_error(
                result["status_code"],
                result["success"],
                result["message"],
            )

        user_response = UserResponse.from_orm(
            result["data"]
        )  # Transform result data into response model
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=user_response,
        )
    except Exception as e:
        # Log the exception (consider adding a logger)
        return raise_error(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,
        )


@router.delete(f"{DELETE_USER_API}" + "{user_id}", response_model=API_Response)
def delete_user_by_id_controller(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),  # Ensure user is authenticated
):
    """
    Controller to delete a user by ID.

    Parameters:
    - user_id: ID of the user to be deleted.
    - db: Database session dependency.
    - user: Authenticated user object.

    Returns:
    - API response with the status of the deletion operation.
    """
    if not isinstance(user, User):  # Check if the authenticated user is valid
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        result = delete_user_by_id_services(db, user_id)
        return create_response(
            result["status_code"],
            result["success"],
            result["message"],
        )
    except Exception as e:
        # Log the exception (consider adding a logger)
        return raise_error(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,
        )
