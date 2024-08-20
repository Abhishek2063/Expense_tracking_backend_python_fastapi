from pydantic import BaseModel

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
    description: str

    class Config:
        """
        Configuration for the UserRoleResponse schema.

        Attributes:
        - orm_mode: Allows Pydantic to work with ORM models by treating them as dictionaries.
        """
        orm_mode = True
        from_attributes=True