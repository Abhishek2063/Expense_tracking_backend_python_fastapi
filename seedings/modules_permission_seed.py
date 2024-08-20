from sqlalchemy.orm import Session
from modals.module_permission_modal import ModulePermission
from utils.common import get_modules, get_roles
from utils.seed_common import get_or_create, seed_data
from modals.roles_modal import Role
from modals.modules_modal import Module

def seed_module_permissions(db: Session):
    """
    Seeds the database with module permissions for different roles.

    - Defines a mapping of roles to modules they should have access to.
    - Retrieves or creates the necessary role and module records.
    - Constructs a list of permissions to be seeded into the database.
    - Uses the `seed_data` function to insert the permissions into the ModulePermission table.

    Parameters:
    - db (Session): The SQLAlchemy database session to use for seeding data.
    """
    # Define a mapping of roles to modules they should have access to
    role_module_map = {
        "Super Admin": ["Dashboard"],
        "Admin": ["Dashboard"],
        "User": ["Dashboard"],
    }

    # List to hold permission records to be inserted
    permissions = []
    
    # Iterate through each role and its associated modules
    for role_name, modules in role_module_map.items():
        # Retrieve or create the role
        role = get_or_create(db, Role, name=role_name)[0]
        
        # Iterate through each module for the current role
        for module_name in modules:
            # Retrieve or create the module
            module = get_or_create(db, Module, name=module_name)[0]
            
            # Append the permission record to the list
            permissions.append(
                {
                    "role_id": role.id,
                    "module_id": module.id,
                }
            )

    # Seed the permissions into the database
    seed_data(db, ModulePermission, permissions)
