from passlib.context import CryptContext
from sqlalchemy.orm import Session
from modals.roles_modal import Role
from modals.modules_modal import Module
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def get_role_by_name(db: Session, role_name: int):
    return db.query(Role).filter(Role.name == role_name).first()

# Function to get all roles with their IDs
def get_roles(db: Session):
    return {role.name: role.id for role in db.query(Role).all()}

# Function to get all modules with their IDs
def get_modules(db: Session):
    return {module.name: module.id for module in db.query(Module).all()}