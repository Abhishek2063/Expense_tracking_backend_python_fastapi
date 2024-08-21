from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy import asc, desc
from schemas.expense_schema import ExpenseCreateSchema, ExpenseResponseSchema
from utils.common import get_category_by_id, get_user_by_id
from utils.message import (
    CATEGORIES_NOT_EXIST,
    EXPENSES_CREATED_SUCCESSFULLY,
    EXPENSES_LIST_GET_SUCCESSFULLY,
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
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
    db.refresh(
        db_expenses
    )  # Refresh the instance to get the updated data from the database

    # Return a success response with the created expense data
    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": EXPENSES_CREATED_SUCCESSFULLY,
        "data": EXPENSES_CREATED_SUCCESSFULLY,
    }


def get_all_expense_by_user_id(
    db: Session,
    user_id: int,
    sort_by: str = "created_at",
    order: str = "desc",
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieve all expenses for a specific user, with options for sorting and pagination.

    Parameters:
    - db (Session): The database session object.
    - user_id (int): The ID of the user whose expenses are to be retrieved.
    - sort_by (str): The field by which to sort the results. Defaults to 'created_at'.
    - order (str): The order of sorting, either 'asc' for ascending or 'desc' for descending. Defaults to 'desc'.
    - skip (int): The number of records to skip (for pagination). Defaults to 0.
    - limit (int): The maximum number of records to return. Defaults to 10.

    Returns:
    - dict: A dictionary containing the success status, status code, message, and the paginated and sorted list of expenses.
    """
    # Validate that the user exists
    user = get_user_by_id(db, user_id)
    if not user:
        # Return an error response if the user does not exist
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Validate the sort field and order to ensure they are acceptable
    valid_sort_by = ["amount", "created_at", "category_id"]
    valid_order = ["asc", "desc"]
    if sort_by not in valid_sort_by:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid sort field specified.",
        }
    if order not in valid_order:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid sort order specified.",
        }

    # Map the sort field to the corresponding database column
    sort_column = {
        "amount": Expense.amount,
        "created_at": Expense.created_at,
        "category_id": Expense.category_id,
    }.get(sort_by, Expense.created_at)

    # Determine the sorting method (ascending or descending)
    order_method = asc if order == "asc" else desc

    # Query the database for the expenses, applying sorting and pagination
    query = (
        db.query(Expense).filter_by(user_id=user_id).order_by(order_method(sort_column))
    )
    total = query.count()
    expenses = query.offset(skip).limit(limit).all()
    total_pages = (
        total + limit - 1
    ) // limit  # Calculate total pages based on count and limit
    current_page = skip // limit + 1  # Calculate the current page number

    # Return a response containing the retrieved expenses and pagination details
    return {
        "success": True,
        "status_code": 200,
        "message": "Expenses retrieved successfully.",
        "data": {
            "total": total,
            "limit": limit,
            "skip": skip,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "expenses": [
                ExpenseResponseSchema.from_orm(expense) for expense in expenses
            ],
        },
    }
