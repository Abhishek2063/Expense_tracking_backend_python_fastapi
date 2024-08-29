from modals.roles_modal import Role
from sqlalchemy.orm import Session

def seed_roles(db: Session):
    """
    Seeds the database with predefined roles.

    - Defines a list of role dictionaries, each containing a name and description.
    - Uses the `seed_data` function to insert the role data into the Role table.

    Parameters:
    - db (Session): The SQLAlchemy database session to use for seeding data.
    """
    # Check if the Role table is empty
    if db.query(Role).count() == 0:
        # Define a list of roles to be seeded into the database
        roles = [
            {"name": "Super Admin", "description": "All access to all features"},
            {"name": "Admin", "description": "Limited access to all features"},
            {"name": "User", "description": "User-related modules permission."},
        ]

        # Insert each role into the database
        for role in roles:
            new_role = Role(**role)
            db.add(new_role)
        
        print("Roles have been seeded successfully.")
    else:
        print("Roles already exist, skipping seeding.")
