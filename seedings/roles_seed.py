from modals.roles_modal import Role
from sqlalchemy.orm import Session
from utils.seed_common import seed_data

def seed_roles(db: Session):
    """
    Seeds the database with predefined roles.

    - Defines a list of role dictionaries, each containing a name and description.
    - Uses the `seed_data` function to insert the role data into the Role table.

    Parameters:
    - db (Session): The SQLAlchemy database session to use for seeding data.
    """
    # Define a list of roles to be seeded into the database
    roles = [
        {"name": "Super Admin", "description": "All access to all features"},
        {"name": "Admin", "description": "Limited access to all features"},
        {"name": "User", "description": "User related modules permission."},
    ]
    
    # Seed the roles into the database using the seed_data function
    seed_data(db, Role, roles)
