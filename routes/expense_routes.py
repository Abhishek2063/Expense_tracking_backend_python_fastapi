from fastapi import APIRouter
from controller.expense_controller import router as expens_router
from utils.api_prefix_list import EXPENSE_API_PREFIX
from utils.api_tag_list import EXPENSE_TAG

# Initialize the main router for expens-related API endpoints
router = APIRouter()

# Include expens routes under the specified prefix and tag
router.include_router(
    expens_router,
    prefix=EXPENSE_API_PREFIX,  # Prefix for all expens-related routes
    tags=[EXPENSE_TAG],  # Tag to group expens-related endpoints
)
