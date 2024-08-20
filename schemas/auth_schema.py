from pydantic import BaseModel, constr, EmailStr, validator
import re
from typing import Optional
from utils.message import USER_PASSWORD_MUST_BE_STRONG
from schemas.role_schema import UserRoleResponse

class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
    - email: The email address of the user.
    - password: The user's password, which must meet strength criteria.
    """
    email: EmailStr  # Email address of the user
    password: constr(min_length=8, max_length=30)  # Password with length constraints

    @validator("password")
    def password_must_be_strong(cls, v):
        """
        Validate that the password meets strength criteria: at least one letter,
        one number, and one special character.
        """
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v
        ):
            raise ValueError(USER_PASSWORD_MUST_BE_STRONG)
        return v

class UserLoginResponse(BaseModel):
    """
    Schema for the user login response.

    Attributes:
    - id: The unique identifier of the user.
    - first_name: The first name of the user.
    - last_name: The last name of the user (optional).
    - email: The email address of the user.
    - role: The role assigned to the user.
    - token: The JWT token for authentication.
    """
    id: int
    first_name: str
    last_name: Optional[str] = None
    email: str
    role: UserRoleResponse
    token: str  # JWT token for authentication

    class Config:
        orm_mode = True  # Allows compatibility with ORM models
        from_attributes = True  # Allows creating models from ORM attributes
