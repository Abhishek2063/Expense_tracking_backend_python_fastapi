from modals.modules_modal import Module
from sqlalchemy.orm import Session

def seed_modules(db:Session):
    try:
        if db.query(Module).count() == 0:
            modules = [
                Module(
                    name="Dashboard",
                    description="All report",
                    link_name="dashboard",
                ),
            ]
            db.add_all(modules)
            db.commit()
            print("Modules seeded successfully")
        else:
            print("Modules already exist, skipping seed.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while seeding modules: {e}")
