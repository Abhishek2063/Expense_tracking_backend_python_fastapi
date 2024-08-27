from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy import asc, desc
from schemas.role_schema import UserRoleCreate, UserRoleResponse, UserRoleUpdate
from utils.common import (
    check_user_role_contained_in_user_table,
    get_role_by_id,
    get_role_by_name,
)
from utils.message import (
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    USER_ROLE_CREATED_SUCCESSFULLY,
    USER_ROLE_DELETE_SUCCESSFULLY,
    USER_ROLE_FOUND_SUCCESSFULL,
    USER_ROLE_IS_CONNECTED_WITH_USER_TABLE,
    USER_ROLE_NAME_ALREADY_TAKEN,
    USER_ROLE_NOT_EXIST,
    USER_ROLE_UPDATE_SUCCESSFULLY,
    USER_ROLES_LIST_GET_SUCCESSFULLY,
)
from modals.roles_modal import Role


def create_role_services(db: Session, role: UserRoleCreate):
    """
    Create a new user role.

    Parameters:
    - db: The database session.
    - role: The data to create a new role.

    Returns:
    - A dictionary with success status, HTTP status code, message, and the created role data.
    """
    # Check if a role with the same name already exists
    db_user_role = get_role_by_name(db, role.name)
    if db_user_role:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": USER_ROLE_NAME_ALREADY_TAKEN,
        }

    # Create and add the new role to the database
    db_user_role = Role(
        name=role.name,
        description=role.description,
    )
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": USER_ROLE_CREATED_SUCCESSFULLY,
        "data": db_user_role,
    }


def get_all_roles_services(
    db: Session,
    sort_by: str = "created_at",
    order: str = "desc",
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieve all user roles with sorting and pagination.

    Parameters:
    - db: The database session.
    - sort_by: Field to sort by (e.g., "name", "created_at").
    - order: Sorting order ("asc" or "desc").
    - skip: Number of records to skip (for pagination).
    - limit: Number of records to return (for pagination).

    Returns:
    - A dictionary with success status, HTTP status code, message, and paginated role data.
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

    # Define sorting column and order method
    sort_column = {
        "name": Role.name,
    }.get(sort_by, Role.name)
    order_method = asc if order == "asc" else desc

    # Query roles with sorting and pagination
    query = db.query(Role).order_by(order_method(sort_column))
    total = query.count()
    roles = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    current_page = skip // limit + 1

    return {
        "success": True,
        "status_code": 200,
        "message": USER_ROLES_LIST_GET_SUCCESSFULLY,
        "data": {
            "total": total,
            "limit": limit,
            "skip": skip,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "roles": [UserRoleResponse.from_orm(role) for role in roles],
        },
    }


def get_role_details_by_id_services(db: Session, role_id: int):
    """
    Retrieve details of a user role by its ID.

    Parameters:
    - db: The database session.
    - role_id: ID of the role to retrieve.

    Returns:
    - A dictionary with success status, HTTP status code, message, and role data.
    """
    # Fetch the role by ID
    role = get_role_by_id(db, role_id)
    if not role:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_ROLE_NOT_EXIST,
        }
    return {
        "success": True,
        "status_code": 200,
        "message": USER_ROLE_FOUND_SUCCESSFULL,
        "data": role,
    }


def role_details_update_services(
    db: Session, role_id: int, user_role_update: UserRoleUpdate
):
    """
    Update a user role's details.

    Parameters:
    - db: The database session.
    - role_id: ID of the role to update.
    - user_role_update: Updated role data.

    Returns:
    - A dictionary with success status, HTTP status code, message, and updated role data.
    """
    # Fetch the role to be updated
    db_user_role = get_role_by_id(db, role_id)
    if not db_user_role:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_ROLE_NOT_EXIST,
        }

    # Check if the new role name is already taken
    if user_role_update.name:
        existing_role = get_role_by_name(db, role_name=user_role_update.name)
        if existing_role:
            return {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": USER_ROLE_NAME_ALREADY_TAKEN,
            }
        # Update the role's name if provided and unique
        db_user_role.name = user_role_update.name

    # Update other fields if provided
    if user_role_update.description:
        db_user_role.description = user_role_update.description

    # Commit the changes to the database
    db.commit()
    db.refresh(db_user_role)

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": USER_ROLE_UPDATE_SUCCESSFULLY,
        "data": db_user_role,
    }


def delete_user_role_by_id_services(db: Session, role_id: int):
    """
    Delete a user role by its ID.

    Parameters:
    - db: The database session.
    - role_id: ID of the role to delete.

    Returns:
    - A dictionary with success status, HTTP status code, and a message.
    """
    # Fetch the role to be deleted
    role = get_role_by_id(db, role_id)
    if not role:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_ROLE_NOT_EXIST,
        }

    # Check if the role is associated with any users
    role_check = check_user_role_contained_in_user_table(db, role_id)
    if role_check:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_ROLE_IS_CONNECTED_WITH_USER_TABLE,
        }

    # Delete the role from the database
    db.delete(role)
    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": USER_ROLE_DELETE_SUCCESSFULLY,
    }
