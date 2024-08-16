from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class ModulePermission(Base):
    __tablename__ = "module_permissions"
    __table_args__ = {"schema": "expanse_tracking_python"}
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    module_id = Column(
        Integer, ForeignKey("expanse_tracking_python.modules.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    role_id = Column(
        Integer, ForeignKey("expanse_tracking_python.roles.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    module = relationship("Module", back_populates="module_permissions")
    role = relationship("Role", back_populates="module_permissions")
    
    