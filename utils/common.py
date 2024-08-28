from passlib.context import CryptContext
from sqlalchemy.orm import Session
from modals.roles_modal import Role
from modals.modules_modal import Module
from modals.users_modal import User
from modals.categories_modal import Category
from modals.expenses_modal import Expense

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


def check_user_role_contained_in_user_table(db: Session, role_id: int):
    """
    Checks if a specific role ID is associated with any user in the User table.

    Args:
        db (Session): The database session used to query the User table.
        role_id (int): The ID of the role to check.

    Returns:
        User: The first User object found with the specified role_id, or None if no user is found.
    """
    return db.query(User).filter(User.role_id == role_id).first()


def get_category_by_id(db: Session, category_id: int) -> Category:
    """
    Retrieve a category from the database by its id.

    Args:
        db (Session): The database session.
        category_id (int): The id of the category to retrieve.

    Returns:
        category: The category object if found, None otherwise.
    """
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_user_id_and_category_name(
    db: Session, user_id: int, category_name: str
):
    """
    Retrieves a category associated with a specific user based on the user's ID and the category's name.

    Args:
        db (Session): The database session used to query the Category table.
        user_id (int): The ID of the user who owns the category.
        category_name (str): The name of the category to retrieve.

    Returns:
        Category: The Category object that matches the user_id and category_name, or None if no match is found.
    """
    return (
        db.query(Category)
        .filter(Category.user_id == user_id, Category.name == category_name)
        .first()
    )


def get_category_by_user_id_and_category_id(
    db: Session, user_id: int, category_id: int
):
    """
    Retrieves a category associated with a specific user based on the user's ID and the category's name.

    Args:
        db (Session): The database session used to query the Category table.
        user_id (int): The ID of the user who owns the category.
        category_id (int): The id of the category to retrieve.

    Returns:
        Category: The Category object that matches the user_id and category_id, or None if no match is found.
    """
    return (
        db.query(Category)
        .filter(Category.user_id == user_id, Category.id == category_id)
        .first()
    )


def get_expense_by_user_id_and_category_id(db: Session, user_id: int, category_id: int):

    return (
        db.query(Expense)
        .filter(Expense.user_id == user_id, Expense.category_id == category_id)
        .first()
    )


def get_module_by_name(db: Session, module_name: str) -> Role:
    """
    Retrieve a module from the database by its name.

    Args:
        db (Session): The database session.
        module_name (str): The name of the module to retrieve.

    Returns:
        module: The module object if found, None otherwise.
    """
    return db.query(Module).filter(Module.name == module_name).first()


def get_module_by_id(db: Session, module_id: int) -> Role:
    """
    Retrieve a module from the database by its id.

    Args:
        db (Session): The database session.
        module_id (int): The id of the module to retrieve.

    Returns:
        module: The module object if found, None otherwise.
    """
    return db.query(Module).filter(Module.id == module_id).first()


def get_expense_by_id(db: Session, expense_id: id) -> Expense:
   
    return db.query(Expense).filter(Expense.id == expense_id).first()