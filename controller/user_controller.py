from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.routes_list import USER_CREATE_API
from schemas.response_schema import API_Response
from schemas.user_schema import User_Create_Schema, UserResponse
from config.database import get_db
from services.user_services import create_user_services
from utils.response import create_response
from utils.message import USER_CREATION_FAILED

router = APIRouter()


@router.post(
    USER_CREATE_API,
    response_model=API_Response,
)
def create_user_controller(
    create_user: User_Create_Schema, db: Session = Depends(get_db)
):
    try:
        db_user = create_user_services(db, create_user)
        if not db_user["success"]:
            return create_response(
                db_user["status_code"],
                db_user["success"],
                db_user["message"],
            )

        user_response = UserResponse.from_orm(db_user["data"])
        return create_response(
            status_code=db_user["status_code"],
            success=db_user["success"],
            message=db_user["message"],
            data=user_response,
        )
    except HTTPException as e:
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        return create_response(
            status_code=500,
            success=False,
            message=USER_CREATION_FAILED,
        )
