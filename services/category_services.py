from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy import asc, desc
from schemas.category_schema import category_create_schema, category_response_schema
from utils.common import get_category_by_user_id_and_category_name, get_user_by_id
from utils.message import (
    CATEGORIES_LIST_GET_SUCCESSFULLY,
    CATEGORY_ALREADY_CREATED,
    CATEGORY_CREATED_SUCCESSFULY,
    INVALID_SORT_FIELD,
    INVALID_SORT_ORDER,
    USER_NOT_EXIST,
)
from modals.categories_modal import Category

def create_category_services(
    db: Session, user_id: int, category_create: category_create_schema
):
    """
    Service to create a new category for a specific user.

    Args:
        db (Session): The database session used to perform operations on the Category and User tables.
        user_id (int): The ID of the user for whom the category is being created.
        category_create (category_create_schema): The data required to create a new category, encapsulated in a schema.

    Returns:
        dict: A dictionary containing the status code, success flag, message, and the created category data.
    """

    # Fetch the user from the database by ID
    user = get_user_by_id(db, user_id)
    if not user:
        # Return an error if the user does not exist
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Check if a category with the same name already exists for the user
    db_category = get_category_by_user_id_and_category_name(
        db, user_id, category_create.name
    )
    if db_category:
        # Return an error if the category already exists
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": CATEGORY_ALREADY_CREATED,
        }

    # Create a new Category instance with the provided data
    db_category = Category(
        name=category_create.name,
        description=category_create.description,
        user_id=user_id,
    )
    
    # Add the new category to the database session and commit the transaction
    db.add(db_category)
    db.commit()
    db.refresh(db_category)  # Refresh the instance to load any updates made during the commit

    # Return a success response with the created category data
    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": CATEGORY_CREATED_SUCCESSFULY,
        "data": db_category,
    }

def get_all_category_services(
    db: Session,
    user_id: int,
    filter_search: str = None,
    sort_by: str = "created_at",
    order: str = "desc",
):
    """
    Retrieves all categories for a specific user, with optional search filtering, sorting, and ordering.

    Args:
        db (Session): The database session used to query the Category table.
        user_id (int): The ID of the user to retrieve categories for.
        filter_search (str, optional): A search string to filter categories by name. Defaults to None.
        sort_by (str, optional): The field to sort the results by. Defaults to "created_at".
        order (str, optional): The order of sorting (ascending or descending). Defaults to "desc".

    Returns:
        dict: A dictionary containing the status code, success flag, message, and data (list of categories).
    """

    # Validate sort field and order
    valid_sort_by = ["name", "created_at"]
    valid_order = ["asc", "desc"]

    if sort_by not in valid_sort_by:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_FIELD,
        }
    if order not in valid_order:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": INVALID_SORT_ORDER,
        }

    # Determine sorting column and order method
    sort_column = {
        "name": Category.name,
        "created_at": Category.created_at,
    }.get(sort_by, Category.created_at)
    order_method = asc if order == "asc" else desc

    # Build the query based on filter_search presence
    if filter_search:
        categories_query = db.query(Category).filter(
            Category.user_id == user_id, Category.name.ilike(f"%{filter_search}%")
        )
    else:
        categories_query = db.query(Category).filter(Category.user_id == user_id)

    # Apply sorting
    categories_query = categories_query.order_by(order_method(sort_column))

    # Execute the query and fetch the results
    categories = categories_query.all()

    return {
        "status_code": status.HTTP_200_OK,
        "success": True,
        "message": CATEGORIES_LIST_GET_SUCCESSFULLY,
        "data": {
            "categories": [
                category_response_schema.from_orm(category) for category in categories
            ],
        },
    }
