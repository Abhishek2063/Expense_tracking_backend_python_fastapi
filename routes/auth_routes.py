from fastapi import APIRouter
from controller.auth_controller import router as auth_router
from utils.api_prefix_list import AUTH_API_PREFIX
from utils.api_tag_list import AUTH_TAG

router = APIRouter()

# To login a user
router.include_router(auth_router, prefix=AUTH_API_PREFIX, tags=[AUTH_TAG])
