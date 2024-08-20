from modals.users_modal import User
from utils.common import get_role_by_name, hash_password
from sqlalchemy.orm import Session
from utils.seed_common import get_or_create, seed_data
from modals.roles_modal import Role

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
            "password_hash": hash_password("Test@1234"),  # Hash the password for storage
            "role_id": get_or_create(db, Role, name="Super Admin")[0].id,  # Get or create the role and use its ID
        },
        {
            "first_name": "Admin",
            "last_name": "",
            "email": "admin@yopmail.com",
            "password_hash": hash_password("Test@1234"),  # Hash the password for storage
            "role_id": get_or_create(db, Role, name="Admin")[0].id,  # Get or create the role and use its ID
        },
        {
            "first_name": "Normal",
            "last_name": "User",
            "email": "testuser@yopmail.com",
            "password_hash": hash_password("Test@1234"),  # Hash the password for storage
            "role_id": get_or_create(db, Role, name="User")[0].id,  # Get or create the role and use its ID
        },
    ]

    # Use the seed_data function to add the users to the database
    seed_data(db, User, users)
