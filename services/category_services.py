from sqlalchemy.orm import Session
from fastapi import status
from sqlalchemy import asc, desc
from schemas.category_schema import (
    category_create_schema,
    category_response_schema,
    category_update_schema,
)
from utils.common import (
    get_category_by_user_id_and_category_id,
    get_category_by_user_id_and_category_name,
    get_expense_by_user_id_and_category_id,
    get_user_by_id,
)
from utils.message import (CATEGORIES_LIST_GET_SUCCESSFULLY, CATEGORIES_NOT_EXIST,
    CATEGORY_ALREADY_CREATED, CATEGORY_CREATED_SUCCESSFULY, CATEGORY_DELETED_SUCCESSFULY,
    CATEGORY_NOT_DELETED, CATEGORY_UPDATED_SUCCESSFULY, INVALID_SORT_FIELD, INVALID_SORT_ORDER,
    USER_NOT_EXIST)
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
    db.refresh(
        db_category
    )  # Refresh the instance to load any updates made during the commit

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
    skip: int = None,
    limit: int = None,
):
    """
    Retrieves all categories for a specific user, with optional search filtering, sorting, ordering, and pagination.

    Args:
        db (Session): The database session used to query the Category table.
        user_id (int): The ID of the user to retrieve categories for.
        filter_search (str, optional): A search string to filter categories by name. Defaults to None.
        sort_by (str, optional): The field to sort the results by. Defaults to "created_at".
        order (str, optional): The order of sorting (ascending or descending). Defaults to "desc".
        skip (int, optional): The number of items to skip (for pagination). Defaults to None.
        limit (int, optional): The maximum number of items to return (for pagination). Defaults to None.

    Returns:
        dict: A dictionary containing the status code, success flag, message, data (list of categories),
            and pagination information if applicable.
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

    # Get total count for pagination
    total_count = categories_query.count()
    # Apply sorting
    categories_query = categories_query.order_by(order_method(sort_column))

    # Initialize pagination variables
    total_pages = None
    current_page = None

    # Apply pagination if both skip and limit are provided
    if skip is not None and limit is not None:
        categories_query = categories_query.offset(skip).limit(limit)
        total_pages = (total_count + limit - 1) // limit
        current_page = skip // limit + 1

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
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": order,
            "total_pages": total_pages,
            "current_page": current_page,
            "filter_search":filter_search
        },
    }


def update_category_services(
    db: Session, user_id: int, category_id: int, category_update: category_update_schema
):
    """
    Service to update an existing category for a specific user.

    Args:
        db (Session): The database session for performing operations on the Category and User tables.
        user_id (int): The ID of the user for whom the category is being updated.
        category_id (int): The ID of the category that needs to be updated.
        category_update (category_update_schema): The data required to update the category, encapsulated in a schema.

    Returns:
        dict: A dictionary containing the status code, success flag, message, and the updated category data.
    """

    # Fetch the user from the database by ID to ensure the user exists
    user = get_user_by_id(db, user_id)
    if not user:
        # Return an error if the user does not exist
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Fetch the category by user ID and category ID to ensure the category exists
    db_category = get_category_by_user_id_and_category_id(db, user_id, category_id)
    if not db_category:
        # Return an error if the category does not exist for the user
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": CATEGORIES_NOT_EXIST,
        }

    # Update the existing category instance with the new data
    db_category.name = category_update.name
    db_category.description = category_update.description

    # Commit the updated category to the database
    db.commit()
    db.refresh(db_category)  # Refresh the instance to reflect the updates

    # Return a success response with the updated category data
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": CATEGORY_UPDATED_SUCCESSFULY,
        "data": db_category,
    }


def delete_category_services(db: Session, user_id: int, category_id: int):
    """
    Service to handle the deletion of a category for a specific user.

    Args:
        db (Session): The database session for performing operations.
        user_id (int): The ID of the user to whom the category belongs.
        category_id (int): The ID of the category to be deleted.

    Returns:
        dict: A dictionary containing the status code, success flag, and message.
    """

    # Fetch the user from the database by ID to ensure the user exists
    user = get_user_by_id(db, user_id)
    if not user:
        # Return an error if the user does not exist
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": USER_NOT_EXIST,
        }

    # Fetch the category by user ID and category ID to ensure the category exists
    db_category = get_category_by_user_id_and_category_id(db, user_id, category_id)
    if not db_category:
        # Return an error if the category does not exist
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": CATEGORIES_NOT_EXIST,
        }

    # Check if there are any expenses associated with the category
    db_expense = get_expense_by_user_id_and_category_id(db, user_id, category_id)
    if db_expense:
        # Return an error if the category cannot be deleted due to associated expenses
        return {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": CATEGORY_NOT_DELETED,
        }

    # Proceed to delete the category from the database
    db.delete(db_category)
    db.commit()

    # Return a success response indicating that the category was deleted
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": CATEGORY_DELETED_SUCCESSFULY,
    }
