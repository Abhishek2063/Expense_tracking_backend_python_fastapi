from fastapi import APIRouter
from controller.user_controller import router as user_router
from utils.api_prefix_list import USER_API_PREFIX
from utils.api_tag_list import USER_TAG

router = APIRouter()

# To create a user
router.include_router(user_router, prefix=USER_API_PREFIX, tags=[USER_TAG])
