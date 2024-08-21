from fastapi import APIRouter, Depends, HTTPException, status
from middlewares.auth_middleware import authenticate_user
from sqlalchemy.orm import Session
from utils.routes_list import EXPENSE_CREATE_API
from schemas.response_schema import API_Response
from schemas.expense_schema import ExpenseCreateSchema
from config.database import get_db
from modals.users_modal import User
from utils.response import create_response
from services.expense_services import create_expenses_services
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
        return create_response(
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
            return create_response(
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
        return create_response(
            status_code=e.status_code,
            success=False,
            message=str(e.detail),
        )
    except Exception as e:
        # Handle unexpected server errors and return a generic error response
        return create_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            message=INTERNAL_SERVER_ERROR,
        )
