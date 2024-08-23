from pydantic import BaseModel
from pydantic import BaseModel, constr, validator
from typing import Optional
from utils.message import NAMES_CONTAINS_ONLY_LETTERS

class module_create_schema(BaseModel):
    name: constr(min_length=2, max_length=20)
    link_name: constr(min_length=2, max_length=20)
    description:Optional[constr(min_length=2, max_length=40)] = None
    
    @validator("name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(NAMES_CONTAINS_ONLY_LETTERS)
        return v.title()

class module_update_schema(BaseModel):
    name: Optional[constr(min_length=2, max_length=20)] = None
    link_name: Optional[constr(min_length=2, max_length=20)] = None
    description:Optional[constr(min_length=2, max_length=20)] = None
    
    @validator("name")
    def name_must_contain_only_letters(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(NAMES_CONTAINS_ONLY_LETTERS)
        return v.title()

class module_response_schema(BaseModel):
    """
    Schema for representing a modules in responses.

    Attributes:
    - id: The unique identifier for the module.
    - name: The name of the module.
    - link name: The link name of the module.
    - description: A brief description of the module.
    """
    id: int
    name: str
    link_name: str
    description: Optional[str] = None
    
    class Config:
        """
        Configuration for the module_response_schema schema.

        Attributes:
        - orm_mode: Allows Pydantic to work with ORM models by treating them as dictionaries.
        """
        orm_mode = True
        from_attributes=True
    
class module_list_response_schema(BaseModel):
    """
    Schema for representing a modules in responses.

    Attributes:
    - id: The unique identifier for the module.
    - name: The name of the module.
    - link name: The link name of the module.
    - description: A brief description of the module.
    """
    id: int
    name: str
    link_name: str
    description: Optional[str] = None
    has_permission : bool

    class Config:
        """
        Configuration for the module_response_schema schema.

        Attributes:
        - orm_mode: Allows Pydantic to work with ORM models by treating them as dictionaries.
        """
        orm_mode = True
        from_attributes=True