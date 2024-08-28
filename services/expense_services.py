from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy import asc, desc
from schemas.expense_schema import (
    ExpenseCreateSchema,
    ExpenseResponseSchema,
    ExpenseUpdateSchema,
)
from utils.common import get_category_by_id, get_expense_by_id, get_user_by_id
from utils.message import (
    CATEGORIES_NOT_EXIST,
    EXPENSE_NOT_EXIST,
    EXPENSES_CREATED_SUCCESSFULLY,
    EXPENSES_DELETE_SUCCESSFULLY,
    EXPENSES_LIST_GET_SUCCESSFULLY,
    EXPENSES_UPDATED_SUCCESSFULLY,
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    INVALID_TIME_FRAME,
    USER_NOT_EXIST,
)
from modals.expenses_modal import Expense
from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy import func, extract
from modals.categories_modal import Category


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


def update_expense(
    db: Session, expense_id: int, expense_data: ExpenseUpdateSchema
) -> Dict[str, Any]:
    """
    Update an existing expense entry.

    Args:
        db (Session): The database session.
        expense_id (int): The ID of the expense to update.
        expense_data (ExpenseUpdateSchema): The new data for the expense.
        user_id (int): The ID of the user making the update.

    Returns:
        Dict[str, Any]: A dictionary containing the status of the operation and the updated expense.

    Raises:
        HTTPException: If the expense is not found or if there's a database error.
    """
    # Retrieve the expense by ID
    db_expense = get_expense_by_id(db, expense_id)
    if not db_expense:
        # Return a failure response if the expense is not found
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": EXPENSE_NOT_EXIST,
        }

    # Update the expense with the provided data, excluding unset fields
    update_data = expense_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    # Commit the changes to the database
    db.commit()
    db.refresh(db_expense)

    # Return a success response with the updated expense
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": EXPENSES_UPDATED_SUCCESSFULLY,
        "data": db_expense,  # Returning the updated expense data
    }


def delete_expense(db: Session, expense_id: int) -> Dict[str, Any]:
    """
    Delete an existing expense entry.

    Args:
        db (Session): The database session.
        expense_id (int): The ID of the expense to delete.
        user_id (int): The ID of the user making the deletion.

    Returns:
        Dict[str, Any]: A dictionary containing the status of the operation and the deletion confirmation.

    Raises:
        HTTPException: If the expense is not found or if there's a database error.
    """
    # Retrieve the expense by ID
    db_expense = get_expense_by_id(db, expense_id)
    if not db_expense:
        # Return a failure response if the expense is not found
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": EXPENSE_NOT_EXIST,
        }

    # Delete the expense from the database
    db.delete(db_expense)
    db.commit()

    # Return a success response confirming the deletion
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,  # Use 200 OK for successful deletion
        "message": EXPENSES_DELETE_SUCCESSFULLY,
    }


def get_time_based_expense_data(
    db: Session, user_id: int, time_frame: str = "date"
) -> Dict[str, Any]:
    """
    Get expense data based on the specified time frame (date, month, or year).

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.
        time_frame (str): The time frame for data aggregation ('date', 'month', or 'year').

    Returns:
        Dict[str, Any]: A dictionary containing the aggregated expense data.
    """
    current_date = datetime.now()

    if time_frame == "date":
        # Get data for current month, day by day
        start_date = current_date.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        query = (
            db.query(
                func.date(Expense.date).label("date"),
                func.sum(Expense.amount).label("total"),
            )
            .filter(
                Expense.user_id == user_id, Expense.date.between(start_date, end_date)
            )
            .group_by(func.date(Expense.date))
        )

    elif time_frame == "month":
        # Get data for current year, month by month
        start_date = current_date.replace(month=1, day=1)
        end_date = start_date.replace(year=start_date.year + 1) - timedelta(days=1)
        query = (
            db.query(
                extract("month", Expense.date).label("month"),
                func.sum(Expense.amount).label("total"),
            )
            .filter(
                Expense.user_id == user_id, Expense.date.between(start_date, end_date)
            )
            .group_by(extract("month", Expense.date))
        )

    elif time_frame == "year":
        # Get data for last 5 years
        start_date = current_date.replace(year=current_date.year - 4, month=1, day=1)
        end_date = current_date
        query = (
            db.query(
                extract("year", Expense.date).label("year"),
                func.sum(Expense.amount).label("total"),
            )
            .filter(
                Expense.user_id == user_id, Expense.date.between(start_date, end_date)
            )
            .group_by(extract("year", Expense.date))
        )

    else:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_TIME_FRAME,
        }
    result = query.all()

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,  # Use 200 OK for successful deletion
        "message": f"Expense data retrieved successfully for {time_frame}",
        "data": [{"period": r[0], "total": float(r[1])} for r in result],
    }


def get_category_wise_expense_data(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Get expense data grouped by category.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        Dict[str, Any]: A dictionary containing the category-wise expense data.
    """
    query = (
        db.query(
            Category.name.label("category"), func.sum(Expense.amount).label("total")
        )
        .join(Expense)
        .filter(Expense.user_id == user_id)
        .group_by(Category.name)
    )

    result = query.all()
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Category-wise expense data retrieved successfully",
        "data": [{"category": r[0], "total": float(r[1])} for r in result],
    }


def get_annual_expense_data(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Get annual expense data for the user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        Dict[str, Any]: A dictionary containing the annual expense data.
    """
    query = (
        db.query(
            extract("year", Expense.date).label("year"),
            func.sum(Expense.amount).label("total"),
        )
        .filter(Expense.user_id == user_id)
        .group_by(extract("year", Expense.date))
        .order_by(extract("year", Expense.date))
    )

    result = query.all()
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Annual expense data retrieved successfully",
        "data": [{"year": int(r[0]), "total": float(r[1])} for r in result],
    }


def get_monthly_expense_data(
    db: Session, user_id: int, year: int = None
) -> Dict[str, Any]:
    """
    Get monthly expense data for the user, optionally for a specific year.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.
        year (int, optional): The year for which to retrieve data. If None, uses the current year.

    Returns:
        Dict[str, Any]: A dictionary containing the monthly expense data.
    """
    if year is None:
        year = datetime.now().year

    query = (
        db.query(
            extract("month", Expense.date).label("month"),
            func.sum(Expense.amount).label("total"),
        )
        .filter(Expense.user_id == user_id, extract("year", Expense.date) == year)
        .group_by(extract("month", Expense.date))
        .order_by(extract("month", Expense.date))
    )

    result = query.all()
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": f"Monthly expense data for year {year} retrieved successfully",
        "data": [{"month": int(r[0]), "total": float(r[1])} for r in result],
    }
