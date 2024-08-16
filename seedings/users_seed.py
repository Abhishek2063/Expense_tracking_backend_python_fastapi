from modals.users_modal import User
from utils.common import get_role_by_name, hash_password
from sqlalchemy.orm import Session

def seed_users(db:Session):
    try:
        if db.query(User).count() == 0:
            users = [
                User(
                    first_name="Super",
                    last_name="Admin",
                    email="superadmin@yopmail.com",
                    password_hash=hash_password("Test@1234"),
                    role_id=get_role_by_name(db, "Super Admin").id
                ),
                User(
                    first_name="Admin",
                    last_name="",
                    email="admin@yopmail.com",
                    password_hash=hash_password("Test@1234"),
                    role_id=get_role_by_name(db, "Admin").id
                ),
                User(
                    first_name="Normal",
                    last_name="User",
                    email="testuser@yopmail.com",
                    password_hash=hash_password("Test@1234"),
                    role_id=get_role_by_name(db, "User").id
                ),
            ]
            db.add_all(users)
            db.commit()
            print("Users seeded successfully")
        else:
            print("Users already exist, skipping seed.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while seeding users: {e}")
