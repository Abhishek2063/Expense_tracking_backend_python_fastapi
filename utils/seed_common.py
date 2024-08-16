from config.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def get_or_create(db: Session, model, defaults=None, **kwargs):
    """Get an existing object or create a new one."""
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        try:
            db.add(instance)
            db.commit()
            return instance, True
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error occurred while creating {model.__name__}: {e}")
            return None, False

def seed_data(db: Session, model, data_list):
    """Seed a list of data into the given model."""
    for data in data_list:
        instance, created = get_or_create(db, model, **data)
        if created:
            print(f"{model.__name__} with {data} created.")
        else:
            print(f"{model.__name__} with {data} already exists, skipping.")
