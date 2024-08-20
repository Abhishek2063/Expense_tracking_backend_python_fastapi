from pydantic import BaseModel
from pydantic import BaseModel, constr, validator
from typing import Optional
from utils.message import NAMES_CONTAINS_ONLY_LETTERS

class UserRoleCreate(BaseModel):
    name: constr(min_length=2, max_length=20)
    description:Optional[constr(min_length=2, max_length=40)] = None
    
    @validator("name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(NAMES_CONTAINS_ONLY_LETTERS)
        return v.title()

class UserRoleUpdate(BaseModel):
    name: Optional[constr(min_length=2, max_length=20)] = None
    description:Optional[constr(min_length=2, max_length=20)] = None
    
    @validator("name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(NAMES_CONTAINS_ONLY_LETTERS)
        return v.title()

class UserRoleResponse(BaseModel):
    """
    Schema for representing a user's role in responses.

    Attributes:
    - id: The unique identifier for the role.
    - name: The name of the role.
    - description: A brief description of the role.
    """
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        """
        Configuration for the UserRoleResponse schema.

        Attributes:
        - orm_mode: Allows Pydantic to work with ORM models by treating them as dictionaries.
        """
        orm_mode = True
        from_attributes=True