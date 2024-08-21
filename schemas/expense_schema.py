from pydantic import BaseModel, constr, validator, Field
from typing import Optional
from datetime import datetime
from schemas.category_schema import category_response_schema

class ExpenseCreateSchema(BaseModel):
    """
    Schema for creating an expense entry.
    
    Attributes:
        user_id (int): The ID of the user who made the expense.
        category_id (int): The ID of the category under which the expense is categorized.
        amount (float): The amount of the expense. Must be greater than 0.
        description (str, optional): A brief description of the expense. 
                                      Must be between 2 to 40 characters.
        date (datetime): The date when the expense was made.
    """
    user_id: int
    category_id: int
    amount: float = Field(..., gt=0, description="The amount of the expense must be greater than 0")
    description: Optional[constr(min_length=2, max_length=40)] = None
    date: datetime

    @validator('amount')
    def validate_amount(cls, v):
        """
        Validate that the amount is a positive number.

        Args:
            v (float): The amount to validate.

        Returns:
            float: The validated amount if it is positive.

        Raises:
            ValueError: If the amount is not greater than 0.
        """
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


class ExpenseUpdateSchema(BaseModel):
    """
    Schema for updating an expense entry.
    
    Attributes:
        user_id (int, optional): The ID of the user who made the expense.
        category_id (int, optional): The ID of the category under which the expense is categorized.
        amount (float, optional): The amount of the expense. Must be greater than 0 if provided.
        description (str, optional): A brief description of the expense. 
                                      Must be between 2 to 40 characters if provided.
        date (datetime, optional): The date when the expense was made.
    """
    user_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[float] = Field(None, gt=0, description="The amount of the expense must be greater than 0 if provided")
    description: Optional[constr(min_length=2, max_length=40)] = None
    date: Optional[datetime] = None

    @validator('amount')
    def validate_amount(cls, v):
        """
        Validate that the amount is a positive number if provided.

        Args:
            v (float): The amount to validate.

        Returns:
            float: The validated amount if it is positive.

        Raises:
            ValueError: If the amount is not greater than 0.
        """
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than 0 if provided')
        return v

class ExpenseResponseSchema(BaseModel):
    category : category_response_schema
    amount : float
    description : Optional[str] = None
    date : datetime
    
    class Config:
        """
        Pydantic configuration for the schema.
        
        Attributes:
            orm_mode (bool): Enable ORM mode for compatibility with ORMs like SQLAlchemy.
            from_attributes (bool): Allow conversion from attribute-based models.
        """
        orm_mode = True
        from_attributes = True
