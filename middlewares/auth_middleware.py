from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional
from config.database import get_db
from utils.message import (
    ACCESS_FORBIDDEN,
    EXPIRED_AUTHORIZATION_TOKEN,
    INVALID_AUTHORIZATION_TOKEN,
    MISSING_AUTHORIZATION_TOKEN,
)
from config.config import settings
from utils.common import get_role_by_id, get_user_by_email
from middlewares.api_permission_middleware import api_permission_check

# Define the OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Authenticate and authorize a user based on the provided JWT token.

    This function performs the following steps:
    1. Extracts and decodes the JWT token from the request.
    2. Validates the presence and integrity of user data within the token.
    3. Retrieves the corresponding user and role information from the database.
    4. (Optional) Checks if the user has permission to access the requested resource.
    5. Handles various authentication errors and returns appropriate responses.

    Parameters:
        request (Request): The incoming HTTP request object.
        token (Optional[str]): The JWT token extracted from the request header.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the authentication result. On success, returns user information;
              on failure, returns an error message with appropriate status code.
    """
    # Check if the token is present in the request
    if token is None:
        return {
            "success": False,
            "status_code": 401,
            "message": MISSING_AUTHORIZATION_TOKEN,
        }

    try:
        # Decode the JWT token to extract payload
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_sub": False},  # Disable 'sub' claim verification for flexibility
        )

        # Extract user information from the token payload
        user_data = payload.get("sub")  # 'sub' claim should contain user details
        if not user_data:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }

        user_id = user_data.get("id")
        user_email = user_data.get("email")
        role_id = user_data.get("role_id")

        # Validate that all necessary user information is present
        if not all([user_id, user_email, role_id]):
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }

        # Retrieve user from the database using email
        user = get_user_by_email(db, user_email)
        if user is None:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }

        # Retrieve user role from the database using role_id
        user_role = get_role_by_id(db, role_id)
        if user_role is None:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }

        # Optional: Check if the user has permission to access the requested resource
        # has_permission = await api_permission_check(user_role.name, request, db)
        # if not has_permission:
        #     return {
        #         "success": False,
        #         "status_code": 403,
        #         "message": ACCESS_FORBIDDEN,
        #     }

        # Authentication successful; return user information
        return user

    except JWTError as e:
        # Handle token expiration error specifically
        if "expired" in str(e):
            return {
                "success": False,
                "status_code": 401,
                "message": EXPIRED_AUTHORIZATION_TOKEN,
            }
        # Handle all other JWT errors
        return {
            "success": False,
            "status_code": 401,
            "message": INVALID_AUTHORIZATION_TOKEN,
        }
