from config.database import Base, engine, SessionLocal
from seedings.roles_seed import seed_roles
from seedings.users_seed import seed_users
from seedings.modules_seed import seed_modules
from seedings.modules_permission_seed import seed_module_permissions
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
        # Seed roles
        print("Seeding roles...")
        seed_roles(db)
        db.commit()  # Commit after seeding roles

        # Seed users
        print("Seeding users...")
        seed_users(db)
        db.commit()  # Commit after seeding users

        # Seed modules
        print("Seeding modules...")
        seed_modules(db)
        db.commit()  # Commit after seeding modules

        # Seed module permissions
        print("Seeding module permissions...")
        seed_module_permissions(db)
        db.commit()  # Commit after seeding module permissions

        # Optionally seed categories if needed
        # This can be included here if there's a need to seed categories directly
        # print("Seeding categories...")
        # seed_categories(db)
        # db.commit()  # Commit after seeding categories

        # Commit all changes
        print("All data seeded successfully.")

    except Exception as e:
        # Print any unexpected errors that occur during seeding
        print(f"An unexpected error occurred: {e}")
        # Rollback in case of error
        db.rollback()
    finally:
        # Ensure the database session is closed
        db.close()
