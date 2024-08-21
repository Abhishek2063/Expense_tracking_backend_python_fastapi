from config.database import Base, engine, SessionLocal
from seedings.roles_seed import seed_roles
from seedings.users_seed import seed_users
from modals.categories_modal import Category
from modals.expenses_modal import Expense
from modals.module_permission_modal import ModulePermission
from modals.modules_modal import Module
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


    except Exception as e:
        # Print any unexpected errors that occur during seeding
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the database session is closed
        db.close()
