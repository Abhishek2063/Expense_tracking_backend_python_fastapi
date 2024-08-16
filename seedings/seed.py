from config.database import Base, engine, SessionLocal
from seedings.roles_seed import seed_roles
from seedings.users_seed import seed_users
from seedings.modules_seed import seed_modules
from seedings.modules_permission_seed import seed_module_permissions
from seedings.category_seed import seed_categories
from modals.expenses_modal import Expense

def seed_data():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        seed_roles(db)
        seed_users(db)
        seed_modules(db)
        seed_module_permissions(db)
        seed_categories(db)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        db.close()