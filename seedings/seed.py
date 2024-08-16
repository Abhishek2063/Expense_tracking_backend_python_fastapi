from config.database import Base, engine, get_db, SessionLocal
from modals.roles_modal import Role
from datetime import datetime
from passlib.context import CryptContext
from utils.common import get_role_by_name, hash_password
from modals.users_modal import User

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
            # Remove all existing roles
        db.query(Role).delete()
        db.commit()
        
        # Seed User Roles
        if db.query(Role).count() == 0:
            roles = [
                Role(
                    name="Super Admin",
                    description="All access to all features",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Role(
                    name="Admin",
                    description="Limited access to all features",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Role(
                    name="User",
                    description="User related modules permission.",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
            ]
            db.add_all(roles)
            db.commit()
            print("roles seeded successfully")
            
        # Seed Users
            
            users = [
            User(
                first_name="super",
                last_name="admin",
                email="superadmin@yopmail.com",
                password_hash=hash_password("Test@1234"),
                role_id=get_role_by_name(db,"Super Admin").id
            ),
            User(
                first_name="Admin",
                last_name="",
                email="admin@yopmail.com",
                password_hash=hash_password("Test@1234"),
                role_id=get_role_by_name(db,"Admin").id
            ),
            User(
                first_name="Normal",
                last_name="User",
                email="testuser@yopmail.com",
                password_hash=hash_password("Test@1234"),
                role_id=get_role_by_name(db,"User").id
            ),
        ]
            
        db.add_all(users)
        db.commit()
        print("users seeded successfully")
    except Exception as e:
        print(f"An error occurred while seeding data: {e}")
    finally:
        db.close()