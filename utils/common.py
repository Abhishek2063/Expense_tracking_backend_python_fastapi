from passlib.context import CryptContext
from sqlalchemy.orm import Session
from modals.roles_modal import Role
from modals.modules_modal import Module
from modals.users_modal import User

# Initialize the CryptContext with bcrypt as the hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the provided plain password matches the hashed password.
    
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password stored in the database.
        
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): The plain text password to hash.
        
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def get_role_by_name(db: Session, role_name: str) -> Role:
    """
    Retrieve a role from the database by its name.
    
    Args:
        db (Session): The database session.
        role_name (str): The name of the role to retrieve.
        
    Returns:
        Role: The Role object if found, None otherwise.
    """
    return db.query(Role).filter(Role.name == role_name).first()

def get_roles(db: Session) -> dict:
    """
    Retrieve all roles from the database and return them as a dictionary.
    
    Args:
        db (Session): The database session.
        
    Returns:
        dict: A dictionary mapping role names to their IDs.
    """
    return {role.name: role.id for role in db.query(Role).all()}

def get_modules(db: Session) -> dict:
    """
    Retrieve all modules from the database and return them as a dictionary.
    
    Args:
        db (Session): The database session.
        
    Returns:
        dict: A dictionary mapping module names to their IDs.
    """
    return {module.name: module.id for module in db.query(Module).all()}

def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve a user from the database by their email address.
    
    Args:
        db (Session): The database session.
        email (str): The email address of the user to retrieve.
        
    Returns:
        User: The User object if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()

def get_role_by_id(db: Session, role_id: int) -> Role:
    """
    Retrieve a role from the database by its id.
    
    Args:
        db (Session): The database session.
        role_id (int): The id of the role to retrieve.
        
    Returns:
        Role: The Role object if found, None otherwise.
    """
    return db.query(Role).filter(Role.id == role_id).first()

def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve a user from the database by its id.
    
    Args:
        db (Session): The database session.
        user_id (int): The id of the user to retrieve.
        
    Returns:
        user: The user object if found, None otherwise.
    """
    return db.query(User).filter(User.id == user_id).first()