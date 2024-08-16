from modals.roles_modal import Role
from sqlalchemy.orm import Session
from utils.seed_common import seed_data

# Seeding Roles
def seed_roles(db: Session):
    roles = [
        {"name": "Super Admin", "description": "All access to all features"},
        {"name": "Admin", "description": "Limited access to all features"},
        {"name": "User", "description": "User related modules permission."},
    ]
    seed_data(db, Role, roles)
