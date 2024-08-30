from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
from datetime import datetime
from modals.categories_modal import Category

# Create a Faker instance
fake = Faker()

# Create a database engine and session
DATABASE_URL = "postgresql://postgres:root@localhost:5432/expanse_tracker"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def insert_random_categories(user_id, count):
    categories = []
    for _ in range(count):
        category_name = fake.word()  # Generate a random category name
        category = Category(
            user_id=user_id,
            name=category_name,
            description=fake.sentence(),  # Random description
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        categories.append(category)
    
    try:
        session.bulk_save_objects(categories)  # Efficient bulk insert
        session.commit()
        print(f"Successfully inserted {count} categories.")
    except Exception as e:
        session.rollback()
        print(f"Error inserting categories: {e}")
    finally:
        session.close()


