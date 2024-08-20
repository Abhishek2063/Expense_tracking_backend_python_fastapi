from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "expanse_tracking_python"}
    
    # Primary key for the User table
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    
    # User's first name, not unique
    first_name = Column(String(20), nullable=False, unique=False)
    
    # User's last name, optional
    last_name = Column(String(20), nullable=True, unique=False)
    
    # User's email, unique across the table
    email = Column(String(255), nullable=False, unique=True)
    
    # Hashed password for the user
    password_hash = Column(String(255), nullable=False)
    
    # Foreign key to the Role table
    role_id = Column(
        Integer, ForeignKey("expanse_tracking_python.roles.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    
    # Token for user authentication (e.g., JWT token)
    token = Column(String(255), nullable=True)
    
    # Timestamps for record creation and updates
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to Role table
    role = relationship("Role", back_populates="users")
    
    # Relationship to Expense table
    expenses = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete, delete-orphan",  # Cascade operations to associated expenses
    )
    
    # Relationship to Report table
    reports = relationship(
        "Report",
        back_populates="user",
        cascade="all, delete, delete-orphan",  # Cascade operations to associated reports
    )
    
    # Relationship to ReminderSetting table
    reminder_settings = relationship(
        "ReminderSetting",
        back_populates="user",
        cascade="all, delete, delete-orphan",  # Cascade operations to associated reminder settings
    )
