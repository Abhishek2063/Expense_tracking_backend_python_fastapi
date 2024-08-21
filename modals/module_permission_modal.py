from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class ModulePermission(Base):
    __tablename__ = "module_permissions"
    __table_args__ = {"schema": "expanse_tracking_python"}

    # Primary key for the ModulePermission table
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # Foreign key to the Module table
    module_id = Column(
        Integer, ForeignKey("expanse_tracking_python.modules.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    

    # Foreign key to the Role table
    role_id = Column(
        Integer, ForeignKey("expanse_tracking_python.roles.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    # Timestamp for when the permission was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Timestamp for when the permission was last updated
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to the Module model
    module = relationship("Module", back_populates="module_permissions")

    # Relationship to the Role model
    role = relationship("Role", back_populates="module_permissions")

