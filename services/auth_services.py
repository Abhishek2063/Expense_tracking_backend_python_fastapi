from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.auth_schema import UserLogin, UserLoginResponse
from utils.common import get_user_by_email, verify_password
from utils.message import INVALID_CREDENTIALS, LOGIN_SUCCESSFUL
from utils.token_generate import create_access_token


def auth_user_services(db: Session, user: UserLogin):
    """
    Authenticate a user by verifying their email and password, then generate and return an access token.

    Args:
        db (Session): The database session.
        user (UserLogin): The schema containing the user's login credentials.

    Returns:
        dict: A dictionary with the result of the authentication operation.
            - success (bool): Indicates if the authentication was successful.
            - status_code (int): The HTTP status code representing the result.
            - message (str): A message providing context about the result.
            - data (User, optional): The authenticated User object, including the access token if the operation was successful.
    """
    # Retrieve the user by email
    db_user = get_user_by_email(db, email=user.email)

    # Check if the user exists
    if not db_user:
        return {
            "success": False,
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": INVALID_CREDENTIALS,
        }

    # Verify the provided password against the stored hashed password
    if not verify_password(user.password, db_user.password_hash):
        return {
            "success": False,
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": INVALID_CREDENTIALS,
        }

    # Prepare user data for JWT token creation
    user_data = {
        "id": str(db_user.id),  # Ensure this is a string
        "email": db_user.email,
        "role_id": str(db_user.role_id),  # Ensure this is a string
    }

    # Generate JWT token with user data
    token = create_access_token(data={"sub": user_data})

    # Store the generated token in the database
    db_user.token = token
    db.commit()

    # Return a success response with the user data including the token
    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": LOGIN_SUCCESSFUL,
        "data": db_user,
    }
