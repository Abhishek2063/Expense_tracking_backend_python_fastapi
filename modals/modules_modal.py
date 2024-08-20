from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Module(Base):
    __tablename__ = "modules"
    __table_args__ = {"schema": "expanse_tracking_python"}

    # Primary key for the Module table
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # Name of the module, unique across the table
    name = Column(String(20), nullable=False, unique=True)

    # Link name for the module, also unique
    link_name = Column(String(20), nullable=False, unique=True)

    # Description of the module
    description = Column(String(255))

    # Timestamp for when the module was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Timestamp for when the module was last updated
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to the ModulePermission model
    module_permissions = relationship(
        "ModulePermission",
        back_populates="module",
        cascade="all, delete, delete-orphan",
    )
