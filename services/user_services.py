from sqlalchemy.orm import Session
from schemas.user_schema import User_Create_Schema, UserResponse
from utils.common import get_role_by_name, get_user_by_email, hash_password
from fastapi import HTTPException, status
from utils.message import (
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    USER_CREATED_SUCCESSFULLY,
    USER_EMAIL_ALREADY_REGISTERED,
    USER_INVALID_ROLE_ID,
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
    valid_sort_by = ["email", "first_name", "last_name", "role", "created_at"]
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

    sort_column = {
        "created_at": User.created_at,
        "email": User.email,
        "first_name": User.first_name,
        "last_name": User.last_name,
        "role": Role.name,
    }.get(sort_by, User.created_at)

    order_method = asc if order == "asc" else desc

    query = (
        db.query(User)
        .join(Role, User.role_id == Role.id)
        .order_by(order_method(sort_column))
    )

    total = query.count()
    users = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    current_page = skip // limit + 1

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
