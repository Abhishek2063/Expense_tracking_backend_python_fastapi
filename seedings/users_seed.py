from modals.users_modal import User
from utils.common import hash_password
from sqlalchemy.orm import Session
from utils.seed_common import get_or_create
from modals.roles_modal import Role
from modals.categories_modal import Category


def seed_users(db: Session):
    """
    Seed the database with initial user data. Creates users with predefined roles and passwords.

    Args:
        db (Session): The database session used to interact with the database.
    """
    # Define a list of users to seed into the database
    users = [
        {
            "first_name": "Super",
            "last_name": "Admin",
            "email": "superadmin@yopmail.com",
            "password_hash": hash_password(
                "Test@1234"
            ),  # Hash the password for storage
            "role_id": get_or_create(db, Role, name="Super Admin")[
                0
            ].id,  # Get or create the role and use its ID
        },
        {
            "first_name": "Admin",
            "last_name": "",
            "email": "admin@yopmail.com",
            "password_hash": hash_password(
                "Test@1234"
            ),  # Hash the password for storage
            "role_id": get_or_create(db, Role, name="Admin")[
                0
            ].id,  # Get or create the role and use its ID
        },
        {
            "first_name": "Normal",
            "last_name": "User",
            "email": "testuser@yopmail.com",
            "password_hash": hash_password(
                "Test@1234"
            ),  # Hash the password for storage
            "role_id": get_or_create(db, Role, name="User")[
                0
            ].id,  # Get or create the role and use its ID
        },
    ]

    # Define default categories for users
    default_categories = [
        {"name": "Food", "description": "Expenses related to food"},
        {"name": "Transport", "description": "Expenses related to transport"},
        {"name": "Entertainment", "description": "Expenses related to entertainment"},
    ]

    # Iterate over each user to check if they already exist in the database
    for user_data in users:
        existing_user = db.query(User).filter_by(email=user_data["email"]).first()
        if existing_user:
            print(f"User '{user_data['email']}' already exists, skipping creation.")
            continue

        # Create and add the new user
        new_user = User(**user_data)
        db.add(new_user)

        # Commit to get the new user ID
        db.commit()
        db.refresh(new_user)

        # Create and add default categories for the new user
        for category_data in default_categories:
            category = Category(
                name=category_data["name"],
                description=category_data["description"],
                user_id=new_user.id,
            )
            db.add(category)

        print(f"User '{user_data['email']}' has been added with default categories.")

    # Commit the session to save the changes
    db.commit()
