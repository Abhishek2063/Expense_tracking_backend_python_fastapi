from sqlalchemy.orm import Session
from schemas.user_schema import User_Create_Schema
from utils.common import get_role_by_name, get_user_by_email, hash_password
from fastapi import HTTPException, status
from utils.message import (
    USER_CREATED_SUCCESSFULLY,
    USER_EMAIL_ALREADY_REGISTERED,
    USER_INVALID_ROLE_ID,
)
from modals.users_modal import User

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
