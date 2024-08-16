from config.database import Base, engine, get_db, SessionLocal
from modals.roles_modal import Role
from datetime import datetime

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Seed User Roles
        if db.query(Role).count() == 0:
            roles = [
                Role(
                    name="Admin",
                    description="Full access to all features",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Role(
                    name="User",
                    description="Can edit and publish, create content",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
            ]
            db.add_all(roles)
            db.commit()
            print("User roles seeded successfully")
    except Exception as e:
        print(f"An error occurred while seeding data: {e}")
    finally:
        db.close()