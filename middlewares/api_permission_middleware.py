from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, Depends
from config.database import get_db
from utils.api_permissions import  API_ROUTES, UserRoles
from utils.message import ACCESS_FORBIDDEN


async def api_permission_check(
    user_role: str,
    request: Request,
    db: Session = Depends(get_db),
):
    api_name = str(request.url.path)
    if api_name:
        
        allowed_roles = API_ROUTES.get(api_name, [])
        
        return UserRoles(user_role) in allowed_roles
    return False
