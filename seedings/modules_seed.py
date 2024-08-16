from modals.modules_modal import Module
from sqlalchemy.orm import Session
from utils.seed_common import seed_data

# Seeding Modules
def seed_modules(db: Session):
    modules = [
        {"name": "Dashboard", "description": "All reports", "link_name": "dashboard"},
    ]
    seed_data(db, Module, modules)
