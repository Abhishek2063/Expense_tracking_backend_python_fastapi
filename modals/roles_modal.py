from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "expanse_tracking_python"}

    # Primary key for the Role table
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    
    # Name of the role (e.g., Super Admin, Admin, User)
    name = Column(String(20), nullable=False, unique=True)
    
    # Description of the role
    description = Column(String(255))
    
    # Timestamps for record creation and updates
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    users = relationship(
        "User",
        back_populates="role",
        cascade="all, delete, delete-orphan",
    )
    module_permissions = relationship(
        "ModulePermission",
        back_populates="role",
        cascade="all, delete, delete-orphan",
    )
