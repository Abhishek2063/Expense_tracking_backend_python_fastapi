from fastapi import APIRouter, Depends, HTTPException, status
from middlewares.auth_middleware import authenticate_user
from sqlalchemy.orm import Session
from utils.routes_list import (
    DELETE_ROLE_BY_ID,
    GET_ALL_ROLE_LIST,
    GET_ROLE_BY_ID,
    ROLE_CREATE_API,
    UPDATE_ROLE_BY_ID,
)
from schemas.response_schema import API_Response
from schemas.role_schema import UserRoleCreate, UserRoleResponse, UserRoleUpdate
from config.database import get_db
from modals.users_modal import User
from utils.response import create_response
from services.role_services import (
    create_role_services,
    delete_user_role_by_id_services,
    get_all_roles_services,
    get_role_details_by_id_services,
    role_details_update_services,
)
from utils.message import INTERNAL_SERVER_ERROR

router = APIRouter()


# API endpoint to create a new user role
@router.post(ROLE_CREATE_API, response_model=API_Response)
def create_new_role_controller(
    role: UserRoleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    # Verify user authentication
    if not isinstance(user, User):
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call service function to create a new role
        db_user_role = create_role_services(db, role)
        if not db_user_role["success"]:
            return create_response(
                db_user_role["status_code"],
                db_user_role["success"],
                db_user_role["message"],
            )

        # Construct response for successful role creation
        user_response = UserRoleResponse.from_orm(db_user_role["data"])
        return create_response(
            status_code=db_user_role["status_code"],
            success=db_user_role["success"],
            message=db_user_role["message"],
            data=user_response,
        )

    except HTTPException as e:
        # Handle HTTP exceptions
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


# API endpoint to list all user roles with optional sorting and pagination
@router.get(GET_ALL_ROLE_LIST, response_model=API_Response)
def list_user_roles_controller(
    sort_by: str = "created_at",
    order: str = "desc",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),  # Ensure user is authenticated
):
    # Verify user authentication
    if not isinstance(user, User):
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call service function to retrieve roles with sorting and pagination
        result = get_all_roles_services(
            db, sort_by=sort_by, order=order, skip=skip, limit=limit
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


# API endpoint to get details of a user role by its ID
@router.get(f"{GET_ROLE_BY_ID}" + "{role_id}", response_model=API_Response)
def get_user_role_controller_by_id(
    role_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),  # Ensure user is authenticated
):
    # Verify user authentication
    if not isinstance(user, User):
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call service function to retrieve role details by ID
        result = get_role_details_by_id_services(db, role_id)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        # Construct response with role details
        user_response = UserRoleResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=user_response,
        )
    except Exception as e:
        # Handle unexpected server errors
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


# API endpoint to update user role details by its ID
@router.put(f"{UPDATE_ROLE_BY_ID}" + "{role_id}", response_model=API_Response)
def update_user_role_details(
    role_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    # Verify user authentication
    if not isinstance(user, User):
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call service function to update role details
        result = role_details_update_services(db, role_id, user_role_update=role_update)
        if not result["success"]:
            return create_response(
                result["status_code"],
                result["success"],
                result["message"],
            )

        # Construct response with updated role details
        user_response = UserRoleResponse.from_orm(result["data"])
        return create_response(
            status_code=result["status_code"],
            success=result["success"],
            message=result["message"],
            data=user_response,
        )
    except Exception as e:
        # Handle unexpected server errors
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


# API endpoint to delete a user role by its ID
@router.delete(f"{DELETE_ROLE_BY_ID}" + "{role_id}", response_model=API_Response)
def delete_user_role_by_id_controller(
    role_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    # Verify user authentication
    if not isinstance(user, User):
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call service function to delete the role
        result = delete_user_role_by_id_services(db, role_id)
        return create_response(
            result["status_code"],
            result["success"],
            result["message"],
        )
    except Exception as e:
        # Handle unexpected server errors
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )
