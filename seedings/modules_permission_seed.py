from sqlalchemy.orm import Session
from modals.module_permission_modal import ModulePermission
from modals.roles_modal import Role
from modals.modules_modal import Module


def seed_module_permissions(db: Session):
    """
    Seeds the database with predefined module permissions for each role.

    Parameters:
    - db (Session): The SQLAlchemy database session to use for seeding data.
    """
    # Retrieve all roles and modules from the database
    roles = db.query(Role).all()
    modules = db.query(Module).all()

    if not roles or not modules:
        print("Roles or modules are missing, skipping module permissions seeding.")
        return

    # Define the module permissions
    module_permissions = [
        # Super Admin has access to all modules
        {"role_name": "Super Admin", "module_ids": [module.id for module in modules]},
        # Admin has limited access (e.g., all but Manage Category and Manage Expense)
        {"role_name": "Admin", "module_ids": [module.id for module in modules]},
        # User has access to only specific modules
        {
            "role_name": "User",
            "module_ids": [
                module.id
                for module in modules
                if module.link_name
                not in [["/manage-module", "/manage-user", "/manage-role"]]
            ],
        },
    ]

    # Seed module permissions
    for permission in module_permissions:
        role = db.query(Role).filter_by(name=permission["role_name"]).first()
        if not role:
            print(f"Role '{permission['role_name']}' not found, skipping permissions.")
            continue

        for module_id in permission["module_ids"]:
            # Check if the permission already exists
            if (
                db.query(ModulePermission)
                .filter_by(role_id=role.id, module_id=module_id)
                .first()
            ):
                continue

            # Create a new ModulePermission object
            new_permission = ModulePermission(role_id=role.id, module_id=module_id)
            db.add(new_permission)

    # Commit the session to save the module permissions
    db.commit()
    print("Module permissions have been seeded successfully.")
