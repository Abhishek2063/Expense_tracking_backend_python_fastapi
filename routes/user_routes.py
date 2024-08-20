from fastapi import APIRouter
from controller.user_controller import router as user_router
from utils.api_prefix_list import USER_API_PREFIX
from utils.api_tag_list import USER_TAG

# Initialize the main router for the API
router = APIRouter()

# Include user-related routes under the specified prefix and tag
router.include_router(
    user_router, 
    prefix=USER_API_PREFIX,  # Prefix for all user-related routes
    tags=[USER_TAG]           # Tag to group user-related endpoints
)
