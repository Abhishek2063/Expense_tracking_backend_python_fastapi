from fastapi import APIRouter
from controller.role_controller import router as role_router
from utils.api_prefix_list import ROLE_API_PREFIX
from utils.api_tag_list import ROLE_TAG

# Initialize the main router for role-related API endpoints
router = APIRouter()

# Include role routes under the specified prefix and tag
router.include_router(
    role_router,
    prefix=ROLE_API_PREFIX,  # Prefix for all role-related routes
    tags=[ROLE_TAG],  # Tag to group role-related endpoints
)
