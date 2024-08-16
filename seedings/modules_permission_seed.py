from sqlalchemy.orm import Session
from modals.module_permission_modal import ModulePermission
from utils.common import get_modules, get_roles
from utils.seed_common import get_or_create, seed_data
from modals.roles_modal import Role
from modals.modules_modal import Module

# Seeding Module Permissions
def seed_module_permissions(db: Session):
    role_module_map = {
        "Super Admin": ["Dashboard"],
        "Admin": ["Dashboard"],
        "User": ["Dashboard"],
    }

    permissions = []
    for role_name, modules in role_module_map.items():
        role = get_or_create(db, Role, name=role_name)[0]
        for module_name in modules:
            module = get_or_create(db, Module, name=module_name)[0]
            permissions.append(
                {
                    "role_id": role.id,
                    "module_id": module.id,
                }
            )

    seed_data(db, ModulePermission, permissions)