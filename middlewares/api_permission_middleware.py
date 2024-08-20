from sqlalchemy.orm import Session
from fastapi import Request, Depends
from config.database import get_db
from utils.api_permissions import API_ROUTES, UserRoles
from utils.message import ACCESS_FORBIDDEN

async def api_permission_check(
    user_role: str,
    request: Request,
    db: Session = Depends(get_db),
) -> bool:
    """
    Checks whether the user has permission to access a specific API route based on their role.

    This function performs the following steps:
    1. Extracts the API route path from the request URL.
    2. Determines the roles allowed to access the extracted API route.
    3. Compares the user's role with the allowed roles for the route.
    4. Returns True if the user has permission; otherwise, returns False.

    Parameters:
        user_role (str): The role of the current user, typically provided as a string.
        request (Request): The incoming HTTP request object from which the API route is extracted.
        db (Session): The database session dependency, which is injected by FastAPI's dependency injection system.

    Returns:
        bool: True if the user's role is authorized to access the API route, otherwise False.
    """
    # Extract the API route path from the request URL
    api_name = str(request.url.path)
    
    if api_name:
        # Retrieve the list of roles allowed to access this API route from the API_ROUTES dictionary
        allowed_roles = API_ROUTES.get(api_name, [])
        
        # Check if the user's role is in the list of allowed roles for this API route
        return UserRoles(user_role) in allowed_roles
    
    # Return False if the API route path is not found or no roles are allowed to access it
    return False
