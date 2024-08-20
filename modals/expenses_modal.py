from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = {"schema": "expanse_tracking_python"}

    # Primary key for the Expense table
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # Foreign key to the User table
    user_id = Column(
        Integer, ForeignKey("expanse_tracking_python.users.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    # Foreign key to the Category table
    category_id = Column(
        Integer, ForeignKey("expanse_tracking_python.categories.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    # Amount of the expense
    amount = Column(Float, nullable=False)

    # Description of the expense
    description = Column(Text, nullable=True)

    # Date when the expense was incurred
    date = Column(DateTime(timezone=True), nullable=False)

    # Timestamp for when the expense was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Timestamp for when the expense was last updated
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to the User model
    user = relationship("User", back_populates="expenses")

    # Relationship to the Category model
    category = relationship("Category", back_populates="expenses")
