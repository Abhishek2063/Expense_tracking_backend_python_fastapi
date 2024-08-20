from fastapi import APIRouter
from controller.auth_controller import router as auth_router
from utils.api_prefix_list import AUTH_API_PREFIX
from utils.api_tag_list import AUTH_TAG

# Initialize the main router for authentication-related API endpoints
router = APIRouter()

# Include authentication routes under the specified prefix and tag
router.include_router(
    auth_router, 
    prefix=AUTH_API_PREFIX,  # Prefix for all authentication-related routes
    tags=[AUTH_TAG]           # Tag to group authentication-related endpoints
)
