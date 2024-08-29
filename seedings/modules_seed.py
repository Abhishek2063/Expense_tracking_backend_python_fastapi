from sqlalchemy.orm import Session
from modals.modules_modal import Module


def seed_modules(db: Session):
    """
    Seeds the database with predefined modules.

    Parameters:
    - db (Session): The SQLAlchemy database session to use for seeding data.
    """
    # Check if the Module table is empty
    if db.query(Module).count() == 0:
        # Define a list of modules to be seeded into the database
        modules = [
            {
                "name": "Dashboard",
                "link_name": "/dashboard",
                "description": "Main dashboard view with overview metrics.",
            },
            {
                "name": "Manage Module",
                "link_name": "/manage-module",
                "description": "Interface for managing application modules.",
            },
            {
                "name": "Manage Role",
                "link_name": "/manage-role",
                "description": "Tool for managing user roles and permissions.",
            },
            {
                "name": "Manage User",
                "link_name": "/manage-user",
                "description": "Admin interface for managing user accounts.",
            },
            {
                "name": "Manage Category",
                "link_name": "/manage-category",
                "description": "Functionality for managing expense categories.",
            },
            {
                "name": "Manage Expense",
                "link_name": "/manage-expense",
                "description": "Tool for recording and tracking expenses.",
            },
        ]

        # Insert each module into the database
        for module in modules:
            new_module = Module(**module)
            db.add(new_module)

        # Commit the session to save the modules
        db.commit()

        print("Modules have been seeded successfully.")
    else:
        print("Modules already exist, skipping seeding.")
