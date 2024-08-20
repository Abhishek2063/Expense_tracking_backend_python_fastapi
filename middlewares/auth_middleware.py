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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    if token is None:
        return {
            "success": False,
            "status_code": 401,
            "message": MISSING_AUTHORIZATION_TOKEN,
        }

    try:

        # Now decode with verification
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_sub": False},  # Disable 'sub' claim verification
        )

        user_data = payload.get("sub")  # 'sub'
        user_id = user_data.get("id")
        user_email = user_data.get("email")
        role_id = user_data.get("role_id")

        if user_email is None or user_id is None or role_id is None:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }

        user = get_user_by_email(db, user_email)
        if user is None:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }
        user_role = get_role_by_id(db, role_id)
        if user_role is None:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }
        has_permission = await api_permission_check(user_role.name, request, db)
        if not has_permission:
            return {
                "success": False,
                "status_code": 403,
                "message": ACCESS_FORBIDDEN,
            }
        return user
    except JWTError as e:
        if "expired" in str(e):
            return {
                "success": False,
                "status_code": 401,
                "message": EXPIRED_AUTHORIZATION_TOKEN,
            }

        else:
            return {
                "success": False,
                "status_code": 401,
                "message": INVALID_AUTHORIZATION_TOKEN,
            }
