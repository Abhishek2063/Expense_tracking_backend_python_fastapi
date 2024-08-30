from fastapi import APIRouter, Depends, HTTPException, status
from middlewares.auth_middleware import authenticate_user
from sqlalchemy.orm import Session
from utils.routes_list import EXPENSE_CREATE_API, EXPENSE_GET_API
from schemas.response_schema import API_Response
from schemas.expense_schema import ExpenseCreateSchema, ExpenseUpdateSchema
from config.database import get_db
from modals.users_modal import User
from utils.response import create_response, raise_error
from services.expense_services import (
    create_expenses_services,
    delete_expense,
    get_all_expense_by_user_id,
    get_annual_expense_data,
    get_category_wise_expense_data,
    get_monthly_expense_data,
    get_time_based_expense_data,
    update_expense,
)
from utils.message import INTERNAL_SERVER_ERROR

# Create an instance of APIRouter to define route operations
router = APIRouter()


@router.post(f"{EXPENSE_CREATE_API}", response_model=API_Response)
def create_new_expense_controller(
    create_expense: ExpenseCreateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Controller for creating a new expense entry.

    This endpoint allows authenticated users to create a new expense.
    It performs the following steps:
    1. Verifies user authentication.
    2. Calls the service layer to create the expense.
    3. Returns the appropriate response based on the outcome of the service.

    Args:
        create_expense (ExpenseCreateSchema): Pydantic schema containing the details of the expense to be created.
        db (Session): SQLAlchemy session dependency for database operations.
        user (User): The authenticated user making the request.

    Returns:
        API_Response: Standardized API response containing the status, success flag, message, and any relevant data.
    """

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response with user details
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Attempt to create a new expense using the service layer
        db_expense = create_expenses_services(db, create_expense)

        # Check if the expense creation was successful
        if not db_expense["success"]:
            # If not successful, return the error response from the service
            return raise_error(
                db_expense["status_code"],
                db_expense["success"],
                db_expense["message"],
            )

        # Return a success response with the newly created expense data
        return create_response(
            status_code=db_expense["status_code"],
            success=db_expense["success"],
            message=db_expense["message"],
            data=db_expense["data"],
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.get(f"{EXPENSE_GET_API}" + "{user_id}", response_model=API_Response)
def get_all_expense_controller(
    user_id: int,
    sort_by: str = "created_at",
    order: str = "desc",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    """
    Controller function to handle the retrieval of all expenses for a specific user.
    This function supports sorting and pagination.

    Parameters:
    - user_id (int): The ID of the user whose expenses are to be retrieved.
    - sort_by (str): The field by which to sort the results. Defaults to 'created_at'.
    - order (str): The order of sorting, either 'asc' for ascending or 'desc' for descending. Defaults to 'desc'.
    - skip (int): The number of records to skip (for pagination). Defaults to 0.
    - limit (int): The maximum number of records to return. Defaults to 10.
    - db (Session): The database session dependency, injected by FastAPI.
    - user (User): The authenticated user, injected by the `authenticate_user` middleware.

    Returns:
    - API_Response: A structured response containing the success status, message, and data (if applicable).
    """

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response with the authentication failure details
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Retrieve all expenses for the specified user using the service layer function
        db_expense = get_all_expense_by_user_id(
            db, user_id=user_id, sort_by=sort_by, order=order, skip=skip, limit=limit
        )

        # Check if the expense retrieval was successful
        if not db_expense["success"]:
            # If not successful, return the error response from the service layer
            return raise_error(
                db_expense["status_code"],
                db_expense["success"],
                db_expense["message"],
            )

        # Return a success response with the retrieved expenses data
        return create_response(
            status_code=db_expense["status_code"],
            success=db_expense["success"],
            message=db_expense["message"],
            data=db_expense["data"],
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions and return the corresponding error response
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.put(f"{EXPENSE_CREATE_API}" + "{expense_id}", response_model=API_Response)
def update_expense_controller(
    expense_id: int,
    expense_data: ExpenseUpdateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
) -> API_Response:
    """
    Update an existing expense entry.

    Args:
        expense_id (int): The ID of the expense to update.
        expense_data (ExpenseUpdateSchema): The new data for the expense.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The authenticated user. Defaults to Depends(authenticate_user).

    Returns:
        API_Response: A standardized response containing the status of the operation and the updated expense.
    """
    # Verify user authentication
    if not isinstance(user, User):
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Attempt to update the expense using the service layer
        db_expense = update_expense(db, expense_id, expense_data, user.id)

        # Check if the update operation was successful
        if not db_expense["success"]:
            return raise_error(
                status_code=db_expense["status_code"],
                success=db_expense["success"],
                message=db_expense["message"],
            )

        # Return a success response with the updated expense data
        return create_response(
            status_code=db_expense["status_code"],
            success=db_expense["success"],
            message=db_expense["message"],
            data=db_expense["data"],
        )

    except HTTPException as e:
        # Handle HTTP-specific exceptions
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.delete(f"{EXPENSE_CREATE_API}" + "{expense_id}", response_model=API_Response)
def delete_expense_controller(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
) -> API_Response:
    """
    Delete an existing expense entry.

    Args:
        expense_id (int): The ID of the expense to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user (User, optional): The authenticated user. Defaults to Depends(authenticate_user).

    Returns:
        API_Response: A standardized response containing the status of the operation and deletion confirmation.
    """
    # Verify user authentication
    if not isinstance(user, User):
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Attempt to delete the expense using the service layer
        db_expense = delete_expense(db, expense_id)

        # Check if the deletion operation was successful
        if not db_expense["success"]:
            return raise_error(
                status_code=db_expense["status_code"],
                success=db_expense["success"],
                message=db_expense["message"],
            )

        # Return a success response confirming the deletion
        return create_response(
            status_code=db_expense["status_code"],
            success=db_expense["success"],
            message=db_expense["message"],
        )

    except HTTPException as e:
        # Handle HTTP-specific exceptions
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.get(
    f"{EXPENSE_GET_API}" + "chart/time-based/{time_frame}" + "/{user_id}",
    response_model=API_Response,
)
def get_time_based_chart_data(
    user_id: int,
    time_frame: str = "date",
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response with the authentication failure details
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Retrieve all expenses for the specified user using the service layer function
        db_expense = get_time_based_expense_data(db, user_id, time_frame)

        # Check if the expense retrieval was successful
        if not db_expense["success"]:
            # If not successful, return the error response from the service layer
            return raise_error(
                db_expense["status_code"],
                db_expense["success"],
                db_expense["message"],
            )

        # Return a success response with the retrieved expenses data
        return create_response(
            status_code=db_expense["status_code"],
            success=db_expense["success"],
            message=db_expense["message"],
            data=db_expense["data"],
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions and return the corresponding error response
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.get(
    f"{EXPENSE_GET_API}" + "chart/category-wise" + "/{user_id}",
    response_model=API_Response,
)
def get_category_wise_chart_data(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response with the authentication failure details
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Retrieve all expenses for the specified user using the service layer function
        db_expense = get_category_wise_expense_data(db, user_id)

        # Check if the expense retrieval was successful
        if not db_expense["success"]:
            # If not successful, return the error response from the service layer
            return raise_error(
                db_expense["status_code"],
                db_expense["success"],
                db_expense["message"],
            )

        # Return a success response with the retrieved expenses data
        return create_response(
            status_code=db_expense["status_code"],
            success=db_expense["success"],
            message=db_expense["message"],
            data=db_expense["data"],
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions and return the corresponding error response
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.get(
    f"{EXPENSE_GET_API}" + "chart/annual" + "/{user_id}", response_model=API_Response
)
def get_annual_chart_data(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response with the authentication failure details
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Retrieve all expenses for the specified user using the service layer function
        db_expense = get_annual_expense_data(db, user_id)

        # Check if the expense retrieval was successful
        if not db_expense["success"]:
            # If not successful, return the error response from the service layer
            return raise_error(
                db_expense["status_code"],
                db_expense["success"],
                db_expense["message"],
            )

        # Return a success response with the retrieved expenses data
        return create_response(
            status_code=db_expense["status_code"],
            success=db_expense["success"],
            message=db_expense["message"],
            data=db_expense["data"],
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions and return the corresponding error response
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )


@router.get(
    f"{EXPENSE_GET_API}" + "chart/monthly" + "/{user_id}", response_model=API_Response
)
def get_monthly_chart_data(
    user_id: int,
    year: int = None,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):

    # Verify user authentication
    if not isinstance(user, User):
        # If the user is not authenticated, return an error response with the authentication failure details
        return raise_error(
            status_code=user["status_code"],
            success=user["success"],
            message=user["message"],
        )

    try:
        # Retrieve all expenses for the specified user using the service layer function
        db_expense = get_monthly_expense_data(db, user_id, year)

        # Check if the expense retrieval was successful
        if not db_expense["success"]:
            # If not successful, return the error response from the service layer
            return raise_error(
                db_expense["status_code"],
                db_expense["success"],
                db_expense["message"],
            )

        # Return a success response with the retrieved expenses data
        return create_response(
            status_code=db_expense["status_code"],
            success=db_expense["success"],
            message=db_expense["message"],
            data=db_expense["data"],
        )

    except HTTPException as e:
        # Handle any HTTP-specific exceptions and return the corresponding error response
        return raise_error(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )
