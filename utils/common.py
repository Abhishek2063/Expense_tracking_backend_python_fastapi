from passlib.context import CryptContext
from sqlalchemy.orm import Session
from modals.roles_modal import Role
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def get_role_by_name(db: Session, role_name: int):
    return db.query(Role).filter(Role.name == role_name).first()