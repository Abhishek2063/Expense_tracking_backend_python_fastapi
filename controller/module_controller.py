from fastapi import APIRouter, Depends, HTTPException, status
from middlewares.auth_middleware import authenticate_user
from sqlalchemy.orm import Session
from utils.routes_list import (
    MODULE_CREATE_API,
    MODULE_GET_API,
    MODULE_PERMISSION_UPDATE_API,
    MODULE_UPDATE_API,
)
from schemas.response_schema import API_Response
from schemas.module_schema import (
    module_create_schema,
    module_response_schema,
    module_update_schema,
)
from config.database import get_db
from modals.users_modal import User
from utils.response import create_response
from services.module_services import (
    create_module_services,
    get_all_modules_list_services,
    update_module_permission_services,
    update_module_services,
)
from utils.message import INTERNAL_SERVER_ERROR

router = APIRouter()


@router.post(f"{MODULE_CREATE_API}", response_model=API_Response)
def create_new_module_controller(
    create_module: module_create_schema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Controller to handle the creation of a new module.

    This endpoint allows an authenticated user to create a new module.
    It first verifies the user's authentication status, then processes the
    module creation request, and returns a structured response.

    Args:
        create_module (module_create_schema): The data required to create a new module.
        db (Session): The database session dependency.
        user (User): The authenticated user, provided by the auth middleware.

    Returns:
        API_Response: A structured response containing the status, success flag, message, and the created module data.
    """

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call the service to create a new module
        db_category = create_module_services(db, create_module)

        # Check if the service returned a success response
        if not db_category["success"]:
            # If the service indicated failure, return the error response
            return create_response(
                db_category["status_code"],
                db_category["success"],
                db_category["message"],
            )

        # Transform the module data into the response schema format
        category_response = module_response_schema.from_orm(db_category["data"])

        # Return the success response with the created module data
        return create_response(
            status_code=db_category["status_code"],
            success=db_category["success"],
            message=db_category["message"],
            data=category_response,
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions that occur during processing
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.put(f"{MODULE_UPDATE_API}" + "{module_id}", response_model=API_Response)
def update_module_controller(
    module_id: int,
    module_update: module_update_schema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Controller to handle the request for updating an existing module.

    This endpoint updates the details of a module based on the provided `module_id`
    and `module_update` schema. It ensures the user is authenticated before processing
    the update and returns the updated module data or an appropriate error message.

    Args:
        module_id (int): The ID of the module to be updated.
        module_update (module_update_schema): The updated data for the module.
        db (Session): The database session used to perform operations.
        user (User): The authenticated user making the request.

    Returns:
        API_Response: A standardized response containing status code, success flag, message,
                      and the updated module data if successful.
    """

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Attempt to update the module using the provided ID and update schema
        db_module = update_module_services(db, module_id, module_update)

        # Check if the service returned a success response
        if not db_module["success"]:
            # If the service indicated failure, return the error response
            return create_response(
                db_module["status_code"],
                db_module["success"],
                db_module["message"],
            )

        # Transform the module data into the response schema format
        module_response = module_response_schema.from_orm(db_module["data"])

        # Return the success response with the updated module data
        return create_response(
            status_code=db_module["status_code"],
            success=db_module["success"],
            message=db_module["message"],
            data=module_response,
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions that occur during processing
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.get(f"{MODULE_GET_API}" + "{role_id}", response_model=API_Response)
def get_all_module_list_controller(
    role_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Controller to fetch a list of all modules and check if a specific role has permissions for each module.

    Args:
        role_id (int): The ID of the role to check permissions for.
        db (Session): The database session used to perform operations.
        user (User): The authenticated user.

    Returns:
        API_Response: A standardized API response object containing status, success flag, message, and module data.
    """

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response with user details
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Fetch modules and their permission status using the service function
        db_module = get_all_modules_list_services(db, role_id)

        # Check if the service returned a success response
        if not db_module["success"]:
            # If the service indicates failure, return the error response
            return create_response(
                db_module["status_code"],
                db_module["success"],
                db_module["message"],
            )

        # Return a success response with the module data
        return create_response(
            status_code=db_module["status_code"],
            success=db_module["success"],
            message=db_module["message"],
            data=db_module["data"],
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions that occur during processing
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.put(
    f"{MODULE_PERMISSION_UPDATE_API}" + "{role_id}/" + "{module_id}",
    response_model=API_Response,
)
def update_module_permission_controller(
    role_id: int,
    module_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Controller to update module permissions for a specific role.

    Args:
        role_id (int): The ID of the role whose permissions are being updated.
        module_id (int): The ID of the module for which permissions are being updated.
        db (Session): The database session used to perform operations.
        user (User): The authenticated user performing the update.

    Returns:
        API_Response: A response object containing the status code, success flag, message, and any relevant data.
    """

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response with user details
        return create_response(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Call the service function to update module permissions
        db_module = update_module_permission_services(db, role_id, module_id)

        # Check if the service returned a success response
        if not db_module["success"]:
            # If the service indicates failure, return the error response
            return create_response(
                status_code=db_module["status_code"],
                success=db_module["success"],
                message=db_module["message"],
            )

        # Return a success response with the module data
        return create_response(
            status_code=db_module["status_code"],
            success=db_module["success"],
            message=db_module["message"],
            data=db_module["data"],
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions that occur during processing
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return create_response(
            status_code=500,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )
