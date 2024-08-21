from fastapi import APIRouter
from controller.category_controller import router as category_router
from utils.api_prefix_list import CATEGORY_API_PREFIX
from utils.api_tag_list import CATEGORY_TAG

# Initialize the main router for category-related API endpoints
router = APIRouter()

# Include category routes under the specified prefix and tag
router.include_router(
    category_router,
    prefix=CATEGORY_API_PREFIX,  # Prefix for all category-related routes
    tags=[CATEGORY_TAG],  # Tag to group category-related endpoints
)
