from pydantic import BaseModel, constr, EmailStr, validator
import re
from typing import Optional
from utils.message import NAMES_CONTAINS_ONLY_LETTERS, USER_PASSWORD_MUST_BE_STRONG
from schemas.role_schema import UserRoleResponse


class User_Create_Schema(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
    - first_name: Required string with a minimum length of 2 and a maximum length of 20.
    - last_name: Optional string with a minimum length of 2 and a maximum length of 20.
    - email: Required email address.
    - password: Required string with a minimum length of 8 and a maximum length of 30.
    """

    first_name: constr(min_length=2, max_length=20)
    last_name: Optional[constr(min_length=2, max_length=20)] = None
    email: EmailStr
    password: constr(min_length=8, max_length=30)

    @validator("first_name", "last_name")
    def name_must_contain_only_letters(cls, v):
        """
        Validate that the first and last names contain only letters and spaces.

        Parameters:
        - v: The value to validate.

        Returns:
        - The validated value with the first letter capitalized.

        Raises:
        - ValueError: If the value contains non-letter characters.
        """
        if not v.replace(" ", "").isalpha():
            raise ValueError(NAMES_CONTAINS_ONLY_LETTERS)
        return v.title()

    @validator("password")
    def password_must_be_strong(cls, v):
        """
        Validate that the password meets strength requirements.

        Parameters:
        - v: The password to validate.

        Returns:
        - The validated password.

        Raises:
        - ValueError: If the password does not meet the strength criteria.
        """
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v
        ):
            raise ValueError(USER_PASSWORD_MUST_BE_STRONG)
        return v


from typing import Optional
from pydantic import BaseModel, constr, validator
import re


# Schema for updating user information
class User_Update_Schema(BaseModel):
    first_name: Optional[constr(min_length=2, max_length=20)] = None
    last_name: Optional[constr(min_length=2, max_length=20)] = None
    role_id: Optional[int] = None

    @validator("first_name", "last_name")
    def name_must_contain_only_letters(cls, v):
        """
        Validate that the first and last names contain only letters and spaces.

        Parameters:
        - v: The value to validate (first_name or last_name).

        Returns:
        - The validated value with the first letter of each word capitalized.

        Raises:
        - ValueError: If the value contains characters other than letters or spaces.
        """
        if not v.replace(" ", "").isalpha():
            raise ValueError(NAMES_CONTAINS_ONLY_LETTERS)
        return v.title()  # Capitalize the first letter of each word


# Schema for updating user password
class UserUpdatePassword(BaseModel):
    current_password: constr(min_length=8, max_length=30)
    new_password: constr(min_length=8, max_length=30)

    @validator("current_password")
    def password_must_be_strong(cls, v):
        """
        Validate that the current password meets the strength requirements.

        Parameters:
        - v: The value to validate (current_password).

        Returns:
        - The validated password if it meets the strength criteria.

        Raises:
        - ValueError: If the password does not meet the strength requirements.
        """
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v
        ):
            raise ValueError(USER_PASSWORD_MUST_BE_STRONG)
        return v

    @validator("new_password")
    def password_must_be_strong(cls, v):
        """
        Validate that the new password meets the strength requirements.

        Parameters:
        - v: The value to validate (new_password).

        Returns:
        - The validated password if it meets the strength criteria.

        Raises:
        - ValueError: If the password does not meet the strength requirements.
        """
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v
        ):
            raise ValueError(USER_PASSWORD_MUST_BE_STRONG)
        return v


class UserResponse(BaseModel):
    """
    Schema for representing a user in responses.

    Attributes:
    - id: The user ID.
    - first_name: The user's first name.
    - last_name: The user's last name (optional).
    - email: The user's email address.
    - role: The user's role information.
    """

    id: int
    first_name: str
    last_name: Optional[str] = None
    email: str
    role: UserRoleResponse

    class Config:
        """
        Configuration for the UserResponse schema.

        Attributes:
        - orm_mode: Enables support for ORM models.
        """

        orm_mode = True
        from_attributes = True
