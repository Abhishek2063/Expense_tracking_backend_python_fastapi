from modals.roles_modal import Role
from sqlalchemy.orm import Session

def seed_roles(db:Session):
    try:
        if db.query(Role).count() == 0:
            roles = [
                Role(
                    name="Super Admin",
                    description="All access to all features",
                ),
                Role(
                    name="Admin",
                    description="Limited access to all features",
                ),
                Role(
                    name="User",
                    description="User related modules permission.",
                ),
            ]
            db.add_all(roles)
            db.commit()
            print("Roles seeded successfully")
        else:
            print("Roles already exist, skipping seed.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while seeding roles: {e}")
