from sqlalchemy.orm import Session
from schemas.user_schema import (
    User_Create_Schema,
    User_Update_Schema,
    UserResponse,
    UserUpdatePassword,
)
from utils.common import (
    get_role_by_id,
    get_role_by_name,
    get_user_by_email,
    get_user_by_id,
    hash_password,
    verify_password,
)
from fastapi import HTTPException, status
from utils.message import (
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    PASSWORD_INCORRECT,
    PASSWORD_UPDATED_SUCCESSFULLY,
    USER_CREATED_SUCCESSFULLY,
    USER_DATA_FOUND,
    USER_DELETED_SUCCESSFULLY,
    USER_EMAIL_ALREADY_REGISTERED,
    USER_INVALID_ROLE_ID,
    USER_NOT_EXIST,
    USER_UPDATED_SUCCESSFULLY,
    USERS_RETRIEVED_SUCCESSFULLY,
)
from modals.users_modal import User
from modals.roles_modal import Role
from sqlalchemy import asc, desc


def create_user_services(db: Session, user_create: User_Create_Schema):
    """
    Service function to create a new user in the database.

    Args:
        db (Session): The database session.
        user_create (User_Create_Schema): The schema containing user details for creation.

    Returns:
        dict: A dictionary with the result of the user creation operation.
            - success (bool): Indicates if the user creation was successful.
            - status_code (int): The HTTP status code representing the result.
            - message (str): A message providing context about the result.
            - data (User, optional): The created User object, if the operation was successful.
    """
    # Check if a user with the provided email already exists
    db_user = get_user_by_email(db, user_create.email)
    if db_user:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": USER_EMAIL_ALREADY_REGISTERED,
        }

    # Retrieve the role by name "User"
    db_role = get_role_by_name(db, role_name="User")
    if not db_role:
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": USER_INVALID_ROLE_ID,
        }

    # Hash the user's password
    hashed_password = hash_password(user_create.password)

    # Create a new User object
    db_user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        password_hash=hashed_password,
        role_id=db_role.id,
    )

    # Add the user to the session and commit to save in the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Return a success response with the created user data
    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": USER_CREATED_SUCCESSFULLY,
        "data": db_user,
    }


def get_all_users_services(
    db: Session,
    sort_by: str = "created_at",
    order: str = "asc",
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieve all users from the database with pagination and sorting options.

    Parameters:
        db (Session): The SQLAlchemy database session.
        sort_by (str): The field by which to sort the users. Default is 'created_at'.
        order (str): The order of sorting, either 'asc' (ascending) or 'desc' (descending). Default is 'asc'.
        skip (int): The number of records to skip for pagination. Default is 0.
        limit (int): The maximum number of records to return. Default is 10.

    Returns:
        dict: A dictionary containing the status of the request, a success flag,
              a message, and the data (user list with pagination details).
    """
    valid_sort_by = ["email", "first_name", "last_name", "role", "created_at"]
    valid_order = ["asc", "desc"]

    # Validate sorting field
    if sort_by not in valid_sort_by:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_FIELD,
        }

    # Validate sorting order
    if order not in valid_order:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_ORDER,
        }

    # Map sorting fields to database columns
    sort_column = {
        "created_at": User.created_at,
        "email": User.email,
        "first_name": User.first_name,
        "last_name": User.last_name,
        "role": Role.name,
    }.get(sort_by, User.created_at)

    # Determine sorting method
    order_method = asc if order == "asc" else desc

    # Construct the query with sorting, pagination, and necessary joins
    query = (
        db.query(User)
        .join(Role, User.role_id == Role.id)
        .order_by(order_method(sort_column))
    )

    # Calculate total records and apply pagination
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    current_page = skip // limit + 1

    # Return response with pagination details and user data
    return {
        "success": True,
        "status_code": 200,
        "message": USERS_RETRIEVED_SUCCESSFULLY,
        "data": {
            "total": total,
            "limit": limit,
            "skip": skip,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "users": [UserResponse.from_orm(user) for user in users],
        },
    }


def get_user_by_id_services(db: Session, user_id: int):
    """
    Retrieve specific user details by user ID.

    Parameters:
        db (Session): The SQLAlchemy database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: A dictionary containing the status of the request, a success flag,
              a message, and the user data if found.
    """
    # Fetch the user from the database by ID
    user = get_user_by_id(db, user_id)
    if not user:
        # Return an error if the user does not exist
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Return the user data if found
    return {
        "success": True,
        "status_code": 200,
        "message": USER_DATA_FOUND,
        "data": user,
    }


# Service to update user details
def update_user_services(db: Session, user_id: int, user_update: User_Update_Schema):
    # Fetch the user by ID
    db_user = get_user_by_id(db, user_id)

    # If the user does not exist, return an error response
    if not db_user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Validate and update the role if a new role ID is provided
    if user_update.role_id:
        role = get_role_by_id(db, user_update.role_id)

        # If the role does not exist, return an error response
        if not role:
            return {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": USER_INVALID_ROLE_ID,
            }

        # Update the user's role
        db_user.role_id = user_update.role_id

    # Update the user's first name if provided
    if user_update.first_name:
        db_user.first_name = user_update.first_name

    # Update the user's last name if provided
    if user_update.last_name:
        db_user.last_name = user_update.last_name

    # Commit the changes to the database and refresh the user object
    db.commit()
    db.refresh(db_user)

    # Return a success response with the updated user data
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": USER_UPDATED_SUCCESSFULLY,
        "data": db_user,
    }


# Service to update user password
def update_user_password_services(
    db: Session, user_id: int, user_update_password: UserUpdatePassword
):
    # Fetch the user by ID
    db_user = get_user_by_id(db, user_id)

    # If the user does not exist, return an error response
    if not db_user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Verify the current password
    if not verify_password(
        user_update_password.current_password, db_user.password_hash
    ):
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": PASSWORD_INCORRECT,
        }

    # Hash and update the new password
    hashed_password = hash_password(user_update_password.new_password)
    db_user.password = hashed_password

    # Commit the changes to the database and refresh the user object
    db.commit()
    db.refresh(db_user)

    # Return a success response with the updated user data
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": PASSWORD_UPDATED_SUCCESSFULLY,
        "data": db_user,
    }


# Service to delete a user by ID
def delete_user_by_id_services(db: Session, user_id: int):
    # Fetch the user by ID
    user = get_user_by_id(db, user_id)

    # If the user does not exist, return an error response
    if not user:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Delete the user from the database
    db.delete(user)
    db.commit()

    # Return a success response confirming the deletion
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": USER_DELETED_SUCCESSFULLY,
    }
