from fastapi import APIRouter
from controller.module_controller import router as module_router
from utils.api_prefix_list import MODULE_API_PREFIX
from utils.api_tag_list import MODULE_TAG

# Initialize the main router for module-related API endpoints
router = APIRouter()

# Include module routes under the specified prefix and tag
router.include_router(
    module_router,
    prefix=MODULE_API_PREFIX,  # Prefix for all module-related routes
    tags=[MODULE_TAG],  # Tag to group module-related endpoints
)
