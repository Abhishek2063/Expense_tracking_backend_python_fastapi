from pydantic import BaseModel, constr, EmailStr, validator
import re
from typing import Optional
from utils.message import USER_PASSWORD_MUST_BE_STRONG
from schemas.role_schema import UserRoleResponse


class UserLogin(BaseModel):
    email: EmailStr  # Correctly annotated as an EmailStr
    password: constr(min_length=8, max_length=30)


    @validator("password")
    def password_must_be_strong(cls, v):
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v
        ):
            raise ValueError(USER_PASSWORD_MUST_BE_STRONG)
        return v


class UserLoginResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    email: str
    role: UserRoleResponse
    token: str

    class Config:
        from_attributes = True
        orm_mode = True
