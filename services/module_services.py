from sqlalchemy.orm import Session, aliased
from fastapi import status
from schemas.module_schema import (
    module_create_schema,
    module_list_response_schema,
    module_response_schema,
    module_update_schema,
)
from utils.common import get_module_by_id, get_module_by_name, get_role_by_id
from utils.message import (
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    MODULE_ALREADY_CREATED,
    MODULE_CREATED_SUCCESSFULLY,
    MODULE_LIST_GET_SUCCESSFULLY,
    MODULE_NOT_EXIST,
    MODULE_PERMISSION_UPDATED_SUCCESSFULLY,
    MODULE_UPDATED_SUCCESSFULLY,
)
from modals.modules_modal import Module
from sqlalchemy import asc, desc, exists, select
from modals.module_permission_modal import ModulePermission


def create_module_services(db: Session, module_create: module_create_schema):
    """
    Service to create a new module.

    This function handles the business logic for creating a new module in the system.
    It first checks if a module with the same name already exists to prevent duplicates.
    If the module does not exist, it proceeds to create and save the new module in the database.

    Args:
        db (Session): The database session used to perform operations on the Module table.
        module_create (module_create_schema): The data required to create a new module, encapsulated in a schema.

    Returns:
        dict: A dictionary containing the status code, success flag, message, and the created module data.
    """

    # Check if a module with the given name already exists in the database
    db_module = get_module_by_name(db, module_create.name)
    if db_module:
        # If the module already exists, return an error response
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": MODULE_ALREADY_CREATED,
        }

    # Create a new module instance with the provided data
    db_module = Module(
        name=module_create.name,
        description=module_create.description,
        link_name=module_create.link_name,
    )

    # Add the new module to the session and commit the transaction
    db.add(db_module)
    db.commit()

    # Refresh the instance to get the latest data from the database
    db.refresh(db_module)

    # Return a success response with the created module's data
    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": MODULE_CREATED_SUCCESSFULLY,
        "data": db_module,
    }


def update_module_services(
    db: Session, module_id: int, module_update: module_update_schema
):
    """
    Service to update an existing module's details.

    This function updates the details of a module in the database, such as its name,
    description, and link name. If the module does not exist, it returns an error response.

    Args:
        db (Session): The database session used for operations.
        module_id (int): The ID of the module to be updated.
        module_update (module_update_schema): The new data to update the module with.

    Returns:
        dict: A dictionary containing the status code, success flag, message, and the updated module data.
    """

    # Check if a module with the given ID exists in the database
    db_module = get_module_by_id(db, module_id)
    if not db_module:
        # If the module does not exist, return an error response
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": MODULE_NOT_EXIST,
        }

    # Update the module's name if provided in the update schema
    if module_update.name:
        db_module.name = module_update.name

    # Update the module's description if provided in the update schema
    if module_update.description:
        db_module.description = module_update.description

    # Update the module's link name if provided in the update schema
    if module_update.link_name:
        db_module.link_name = module_update.link_name

    # Commit the changes to the database and refresh the module object
    db.commit()
    db.refresh(db_module)

    # Return a success response with the updated module's data
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": MODULE_UPDATED_SUCCESSFULLY,
        "data": db_module,
    }


def get_all_modules_list_services(
    db: Session,
    role_id: int,
    sort_by: str = "created_at",
    order: str = "desc",
):
    """
    Fetch all modules and indicate whether the specified role has permission for each module.

    Args:
        db (Session): The database session.
        role_id (int): The role ID to check for permissions.
        sort_by (str): The field to sort the results by.
        order (str): The order to sort the results in (ascending or descending).

    Returns:
        dict: A dictionary containing the status code, success flag, message, and the data.
    """
    # Validate sort field and order
    valid_sort_by = ["name", "created_at"]
    valid_order = ["asc", "desc"]

    if sort_by not in valid_sort_by:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_FIELD,
        }
    if order not in valid_order:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_ORDER,
        }

    # Determine sorting column and order method
    sort_column = {
        "name": Module.name,
        "created_at": Module.created_at,
    }.get(sort_by, Module.created_at)
    order_method = asc if order == "asc" else desc

    # Query to fetch all modules with permission status
    modules_query = db.query(
        Module.id,
        Module.name,
        Module.link_name,
        Module.description,
        exists(
            select(ModulePermission)
            .where(ModulePermission.role_id == role_id)
            .where(ModulePermission.module_id == Module.id)
        ).label("has_permission"),
    ).order_by(order_method(sort_column))

    # Execute the query and fetch results
    modules = modules_query.all()
    if not modules:
        return {
            "status_code": status.HTTP_200_OK,
            "success": True,
            "message": MODULE_LIST_GET_SUCCESSFULLY,
            "data": {
                "modules": [],
            },
        }

    return {
        "status_code": status.HTTP_200_OK,
        "success": True,
        "message": MODULE_LIST_GET_SUCCESSFULLY,
        "data": {
            "modules": [
                module_list_response_schema.from_orm(module) for module in modules
            ],
        },
    }


def update_module_permission_services(
    db: Session,
    role_id: int,
    module_id: int,
):
    """
    Service to update module permissions for a specific role.

    Args:
        db (Session): The database session used to perform operations.
        role_id (int): The ID of the role for which permissions are being updated.
        module_id (int): The ID of the module for which permissions are being updated.

    Returns:
        dict: A dictionary containing the status code, success flag, message, and the updated module data.
    """

    # Check if the module exists in the database
    db_module = get_module_by_id(db, module_id)
    if not db_module:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": MODULE_NOT_EXIST,
        }

    # Check if the role exists in the database
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": MODULE_NOT_EXIST,
        }

    # Check if there is an existing permission entry for the given module and role
    existing_permission = (
        db.query(ModulePermission)
        .filter(
            ModulePermission.module_id == module_id, ModulePermission.role_id == role_id
        )
        .first()
    )

    if existing_permission:
        # If permission exists, delete it
        db.delete(existing_permission)
        db.commit()
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": MODULE_PERMISSION_UPDATED_SUCCESSFULLY,
            "data": {"message": "Permission entry deleted"},
        }
    else:
        # If permission does not exist, insert a new entry
        new_permission = ModulePermission(module_id=module_id, role_id=role_id)
        db.add(new_permission)
        db.commit()
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": MODULE_PERMISSION_UPDATED_SUCCESSFULLY,
            "data": {"message": "Permission entry created"},
        }
