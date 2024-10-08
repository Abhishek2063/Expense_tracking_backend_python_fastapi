from fastapi import FastAPI, status, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from seedings.seed import seed_data
from utils.message import VALIDATION_ERROR, WELCOME_MESSAGE
from utils.response import create_response
from routes.user_routes import router as user_router
from routes.auth_routes import router as auth_router
from routes.role_routes import router as role_router
from routes.category_routes import router as category_router
from routes.module_routes import router as module_router
from routes.expense_routes import router as expense_router
from fastapi.middleware.cors import CORSMiddleware

from middlewares.custom_exception_handler import custom_http_exception_handler
from config.config import settings
# from fakerData.expenseFackerData import insert_random_expenses
# from fakerData.categoryFackerData import insert_random_categories

# Seed initial data into the database (if applicable)
seed_data()

origins = ["*"]

# Initialize the FastAPI application
app = FastAPI()

# Include custom exception handler
app.add_exception_handler(HTTPException, custom_http_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handler for request validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors raised during request validation.

    Args:
        request (Request): The request object that caused the validation error.
        exc (RequestValidationError): The validation error exception.

    Returns:
        JSONResponse: A custom JSON response containing the error details.
    """
    errors = exc.errors()
    formatted_errors = []

    # Format each validation error to include the field and the error message
    for error in errors:
        formatted_errors.append({"field": error["loc"][-1], "message": error["msg"]})

    return JSONResponse(
        status_code=400,
        content={
            "status_code": 400,
            "success": False,
            "message": VALIDATION_ERROR,
            "errors": formatted_errors,
        },
    )


# Include user-related routes from the `user_routes` module
app.include_router(user_router)

# Include authentication-related routes from the `auth_routes` module
app.include_router(auth_router)

# Include role-related routes from the `role_routes` module
app.include_router(role_router)

# Include category-related routes from the `category_routes` module
app.include_router(category_router)

# Include module-related routes from the `module_routes` module
app.include_router(module_router)

# Include expense-related routes from the `expense_routes` module
app.include_router(expense_router)

# # Example usage
# insert_random_categories(user_id=4, count=20)
# Usage
# user_id = 4  # Replace with the actual user ID
# year = 2024  # Replace with the desired year
# num_expenses_per_month = 30  # Adjust as needed

# insert_random_expenses(user_id, year, num_expenses_per_month)
# Define a root endpoint that returns a welcome message
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message when accessed.

    Returns:
        dict: A JSON response with a welcome message.
    """
    return create_response(status.HTTP_200_OK, True, WELCOME_MESSAGE)
