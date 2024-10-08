from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "expanse_tracking_python"}

    # Primary key for the Category table
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    
   # Foreign key to the User table
    user_id = Column(
        Integer, ForeignKey("expanse_tracking_python.users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    # Name of the category
    name = Column(String(20), nullable=False, unique=False)

    # Description of the category
    description = Column(String(255))

    # Timestamp for when the category was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Timestamp for when the category was last updated
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to the Expense model
    expenses = relationship(
        "Expense",
        back_populates="category",
        cascade="all, delete, delete-orphan",
    )
    
    # Relationship to the User model
    user = relationship("User", back_populates="categories")
