from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.auth_schema import UserLogin, UserLoginResponse
from utils.common import get_user_by_email, verify_password
from utils.message import INVALID_CREDENTIALS, LOGIN_SUCCESSFUL
from utils.token_generate import create_access_token

def auth_user_services(db: Session, user: UserLogin):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user:
        return {
            "success": False,
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": INVALID_CREDENTIALS,
        }

    if not verify_password(user.password, db_user.password_hash):
        return {
            "success": False,
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": INVALID_CREDENTIALS,
        }
    # Convert the user to a serializable format
    user_data = {"id": db_user.id, "email": db_user.email}
    # Generate JWT token
    token = create_access_token(data={"sub": user_data})

    # Store token in database
    db_user.token = token
    db.commit()

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": LOGIN_SUCCESSFUL,
        "data": db_user
    }