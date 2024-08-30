from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
from datetime import datetime, timedelta
import random
from modals.categories_modal import Category
from modals.expenses_modal import Expense
from config.config import settings

# Create a Faker instance
fake = Faker()

# Create a database engine and session
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_random_expenses(user_id, year, num_expenses_per_month):
    session = SessionLocal()
    try:
        # Get all categories for the user
        categories = session.query(Category).filter(Category.user_id == user_id).all()
        
        if not categories:
            print(f"No categories found for user_id: {user_id}")
            return

        expenses = []
        
        for month in range(1, 13):  # For each month
            for _ in range(num_expenses_per_month):  # Number of expenses per month
                category = random.choice(categories)
                
                # Generate a random date within the month
                date = datetime(year, month, random.randint(1, 28))
                
                expense = Expense(
                    user_id=user_id,
                    category_id=category.id,
                    amount=round(random.uniform(10, 1000), 2),  # Random amount between 10 and 1000
                    description=fake.sentence(),
                    date=date,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                expenses.append(expense)

        session.bulk_save_objects(expenses)
        session.commit()
        print(f"Successfully inserted {len(expenses)} expenses for user {user_id} in year {year}.")
    except Exception as e:
        session.rollback()
        print(f"Error inserting expenses: {e}")
    finally:
        session.close()

