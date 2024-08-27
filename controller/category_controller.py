from fastapi import APIRouter, Depends, HTTPException, status
from middlewares.auth_middleware import authenticate_user
from sqlalchemy.orm import Session
from utils.routes_list import CATEGORY_CREATE_API, GET_ALL_CATEGORY_LIST
from schemas.response_schema import API_Response
from schemas.category_schema import category_create_schema, category_response_schema
from config.database import get_db
from modals.users_modal import User
from utils.response import create_response
from services.category_services import (
    create_category_services,
    get_all_category_services,
)
from utils.message import INTERNAL_SERVER_ERROR

router = APIRouter()


@router.post(f"{CATEGORY_CREATE_API}" + "{user_id}", response_model=API_Response)
def create_new_category_controller(
    user_id: int,
    create_category: category_create_schema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Endpoint to create a new category for a user.

    Args:
        user_id (int): The ID of the user creating the category.
        create_category (category_create_schema): The schema containing the category details.
        db (Session): The database session dependency.
        user (User): The authenticated user object.

    Returns:
        API_Response: The response object containing the status, success flag, message, and data.
    """

    # Verify user authentication
    if not isinstance(user, User):
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Attempt to create a new category using the service layer
        db_category = create_category_services(db, user_id, create_category)

        # Check if the category creation was successful
        if not db_category["success"]:
            return create_response(
                db_category["status_code"],
                db_category["success"],
                db_category["message"],
            )

        # Transform the category data into the response schema format
        category_response = category_response_schema.from_orm(db_category["data"])
        return create_response(
            status_code=db_category["status_code"],
            success=db_category["success"],
            message=db_category["message"],
            data=category_response,
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.get(f"{GET_ALL_CATEGORY_LIST}" + "{user_id}", response_model=API_Response)
def get_all_category_controller(
    user_id: int,
    filter_search: str = None,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),  # Ensure user is authenticated
):
    """
    Endpoint to retrieve a list of categories for a user, with optional filtering and sorting.

    Args:
        user_id (int): The ID of the user whose categories are to be retrieved.
        filter_search (str): Optional search string to filter categories.
        sort_by (str): The field by which the categories should be sorted. Defaults to "created_at".
        order (str): The sorting order, either "asc" or "desc". Defaults to "desc".
        db (Session): The database session dependency.
        user (User): The authenticated user object.

    Returns:
        API_Response: The response object containing the status, success flag, message, and data.
    """

    # Verify user authentication
    if not isinstance(user, User):
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Retrieve the categories using the service layer with provided filters and sorting
        result = get_all_category_services(
            db, user_id, filter_search, sort_by=sort_by, order=order
        )
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=result["data"],
        )
    except Exception as e:
        # Handle unexpected server errors
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )
