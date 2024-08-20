from enum import Enum
from utils.api_prefix_list import AUTH_API_PREFIX, USER_API_PREFIX
from utils.routes_list import GET_ALL_USERS_LIST_WITH_PAGINATION, LOGIN_API, USER_CREATE_API

class UserRoles(Enum):
    SUPER_ADMIN = "Super Admin"
    ADMIN = "Admin"
    USER = "User"


# Combine prefixes and routes
API_ROUTES = {
    f"{USER_API_PREFIX}{USER_CREATE_API}": [UserRoles.SUPER_ADMIN, UserRoles.ADMIN, UserRoles.USER],
    f"{USER_API_PREFIX}{GET_ALL_USERS_LIST_WITH_PAGINATION}": [UserRoles.SUPER_ADMIN, UserRoles.ADMIN, UserRoles.USER],
    f"{AUTH_API_PREFIX}{LOGIN_API}": [UserRoles.SUPER_ADMIN, UserRoles.ADMIN, UserRoles.USER],
}

