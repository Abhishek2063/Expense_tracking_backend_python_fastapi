from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy import asc, desc
from schemas.expense_schema import ExpenseCreateSchema
from utils.common import get_category_by_id, get_user_by_id
from utils.message import (
    CATEGORIES_NOT_EXIST,
    EXPENSES_CREATED_SUCCESSFULLY,
    USER_NOT_EXIST,
)
from modals.expenses_modal import Expense


def create_expenses_services(db: Session, expenses_create: ExpenseCreateSchema):
    """
    Service to create a new expense entry in the database.

    This function performs the following steps:
    1. Validates that the user associated with the expense exists.
    2. Validates that the category associated with the expense exists.
    3. Creates a new expense entry in the database.

    Args:
        db (Session): SQLAlchemy session for database operations.
        expenses_create (ExpenseCreateSchema): Pydantic schema containing the expense details.

    Returns:
        dict: A dictionary containing the status code, success flag, message, and optionally the created expense data.

    Raises:
        HTTPException: If the user or category does not exist.
    """

    # Validate that the user exists
    user = get_user_by_id(db, expenses_create.user_id)
    if not user:
        # Return an error response if the user does not exist
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Validate that the category exists
    db_category = get_category_by_id(db, expenses_create.category_id)
    if not db_category:
        # Return an error response if the category does not exist
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": CATEGORIES_NOT_EXIST,
        }

    # Create a new Expense instance with the provided data
    db_expenses = Expense(
        user_id=expenses_create.user_id,
        category_id=expenses_create.category_id,
        amount=expenses_create.amount,
        description=expenses_create.description,
        date=expenses_create.date,
    )

    # Add the expense to the session and commit the transaction
    db.add(db_expenses)
    db.commit()
    db.refresh(db_expenses)  # Refresh the instance to get the updated data from the database

    # Return a success response with the created expense data
    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": EXPENSES_CREATED_SUCCESSFULLY,
        "data": EXPENSES_CREATED_SUCCESSFULLY,
    }
