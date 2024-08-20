from sqlalchemy.orm import Session
from utils.seed_common import seed_data
from modals.categories_modal import Category

def seed_categories(db: Session):
    """
    Seeds the database with predefined categories.

    - Defines a list of categories with their names and descriptions.
    - Uses the `seed_data` function to insert the categories into the Category table.

    Parameters:
    - db (Session): The SQLAlchemy database session to use for seeding data.
    """
    # Define a list of categories with their names and descriptions
    categories = [
        {"name": "Groceries", "description": "Daily groceries and essentials"},
        {"name": "Utilities", "description": "Monthly utility bills"},
        {"name": "Entertainment", "description": "Movies, games, and other entertainment expenses"},
        {"name": "Transport", "description": "Transportation costs"},
        {"name": "Healthcare", "description": "Healthcare-related expenses"},
    ]

    # Seed the categories into the database
    seed_data(db, Category, categories)
