from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Module(Base):
    __tablename__ = "modules"
    __table_args__ = {"schema": "expanse_tracking_python"}
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(20), nullable=False, unique=True)
    link_name = Column(String(20), nullable=False, unique=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    