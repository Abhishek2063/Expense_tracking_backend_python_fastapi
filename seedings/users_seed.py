from modals.users_modal import User
from utils.common import get_role_by_name, hash_password
from sqlalchemy.orm import Session
from utils.seed_common import get_or_create, seed_data
from modals.roles_modal import Role

# Seeding Users
def seed_users(db: Session):
    users = [
        {
            "first_name": "Super",
            "last_name": "Admin",
            "email": "superadmin@yopmail.com",
            "password_hash": hash_password("Test@1234"),
            "role_id": get_or_create(db, Role, name="Super Admin")[0].id,
        },
        {
            "first_name": "Admin",
            "last_name": "",
            "email": "admin@yopmail.com",
            "password_hash": hash_password("Test@1234"),
            "role_id": get_or_create(db, Role, name="Admin")[0].id,
        },
        {
            "first_name": "Normal",
            "last_name": "User",
            "email": "testuser@yopmail.com",
            "password_hash": hash_password("Test@1234"),
            "role_id": get_or_create(db, Role, name="User")[0].id,
        },
    ]
    seed_data(db, User, users)