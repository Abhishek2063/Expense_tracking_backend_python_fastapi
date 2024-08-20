from pydantic import BaseModel, constr, EmailStr, validator
import re
from typing import Optional
from utils.message import NAMES_CONTAINS_ONLY_LETTERS, USER_PASSWORD_MUST_BE_STRONG
from schemas.role_schema import UserRoleResponse

class User_Create_Schema(BaseModel):
    first_name: constr(min_length=2, max_length=20)
    last_name: Optional[constr(min_length=2, max_length=20)] = None
    email: EmailStr  # Correctly annotated as an EmailStr
    password: constr(min_length=8, max_length=30)

    @validator("first_name", "last_name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(NAMES_CONTAINS_ONLY_LETTERS)
        return v.title()

    @validator("password")
    def password_must_be_strong(cls, v):
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v
        ):
            raise ValueError(USER_PASSWORD_MUST_BE_STRONG)
        return v


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    email: str
    role: UserRoleResponse

    class Config:
        from_attributes = True
        orm_mode = True
