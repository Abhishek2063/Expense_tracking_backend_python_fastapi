from modals.modules_modal import Module
from sqlalchemy.orm import Session
from utils.seed_common import seed_data

def seed_modules(db: Session):
    """
    Seeds the database with predefined modules.

    - Defines a list of module dictionaries, each containing a name, description, and link name.
    - Uses the `seed_data` function to insert the module data into the Module table.

    Parameters:
    - db (Session): The SQLAlchemy database session to use for seeding data.
    """
    # Define a list of modules to be seeded into the database
    modules = [
        {"name": "Dashboard", "description": "All reports", "link_name": "dashboard"},
    ]
    
    # Seed the modules into the database using the seed_data function
    seed_data(db, Module, modules)
