from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "expanse_tracking_python"}
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String(20), nullable=False, unique=False)
    last_name = Column(String(20), nullable=True, unique=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(
        Integer, ForeignKey("expanse_tracking_python.roles.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    token = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    role = relationship("Role", back_populates="users")
    expenses = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete, delete-orphan",
    )
    