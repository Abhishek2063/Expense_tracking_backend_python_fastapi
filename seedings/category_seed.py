from sqlalchemy.orm import Session
from utils.seed_common import seed_data
from modals.categories_modal import Category


# Seeding Categories
def seed_categories(db: Session):
    categories = [
        {"name": "Groceries", "description": "Daily groceries and essentials"},
        {"name": "Utilities", "description": "Monthly utility bills"},
        {"name": "Entertainment", "description": "Movies, games, and other entertainment expenses"},
        {"name": "Transport", "description": "Transportation costs"},
        {"name": "Healthcare", "description": "Healthcare-related expenses"},
    ]
    seed_data(db, Category, categories)
