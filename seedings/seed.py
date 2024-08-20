from config.database import Base, engine, SessionLocal
from seedings.roles_seed import seed_roles
from seedings.users_seed import seed_users
from seedings.modules_seed import seed_modules
from seedings.modules_permission_seed import seed_module_permissions
from seedings.category_seed import seed_categories
from modals.expenses_modal import Expense
from modals.reports_modal import Report
from modals.settings_modal import ReminderSetting

def seed_data():
    """
    Seeds the database with initial data by creating tables and inserting predefined records.

    - Creates all tables defined in the Base metadata.
    - Seeds roles, users, modules, module permissions, and categories into the database.
    """
    # Create all tables defined in the Base metadata
    Base.metadata.create_all(bind=engine)

    # Create a new database session
    db = SessionLocal()

    try:
        # Seed the database with roles
        seed_roles(db)
        # Seed the database with users
        seed_users(db)
        # Seed the database with modules
        seed_modules(db)
        # Seed the database with module permissions
        seed_module_permissions(db)
        # Seed the database with categories
        seed_categories(db)
    except Exception as e:
        # Print any unexpected errors that occur during seeding
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the database session is closed
        db.close()
