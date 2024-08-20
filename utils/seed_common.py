from config.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def get_or_create(db: Session, model, defaults=None, **kwargs):
    """
    Retrieve an existing object from the database or create a new one if it doesn't exist.

    Args:
        db (Session): The database session.
        model: The SQLAlchemy model class.
        defaults (dict, optional): A dictionary of default values to use when creating the object.
        **kwargs: The criteria used to filter the model and find the object.

    Returns:
        tuple: A tuple containing the object instance and a boolean indicating if it was created (True) or retrieved (False).
    """
    # Attempt to find an existing object matching the given criteria
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        # If found, return the instance and False (indicating it wasn't created)
        return instance, False
    else:
        # If not found, create a new instance with the given parameters
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        try:
            # Try to add the new instance to the database and commit the transaction
            db.add(instance)
            db.commit()
            return instance, True  # Return the new instance and True (indicating it was created)
        except SQLAlchemyError as e:
            # If an error occurs, roll back the transaction and log the error
            db.rollback()
            print(f"Error occurred while creating {model.__name__}: {e}")
            return None, False  # Return None and False (indicating creation failed)

def seed_data(db: Session, model, data_list):
    """
    Seed a list of data into the given model, creating objects if they don't already exist.

    Args:
        db (Session): The database session.
        model: The SQLAlchemy model class.
        data_list (list): A list of dictionaries, each containing the data to be seeded into the model.

    """
    # Iterate over each data item in the list
    for data in data_list:
        # Use get_or_create to either retrieve or create the object
        instance, created = get_or_create(db, model, **data)
        if created:
            # If the object was created, log a message indicating success
            print(f"{model.__name__} with {data} created.")
        else:
            # If the object already exists, log a message indicating it was skipped
            print(f"{model.__name__} with {data} already exists, skipping.")
