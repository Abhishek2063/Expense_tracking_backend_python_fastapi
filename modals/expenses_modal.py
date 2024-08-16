from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Float,Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = {"schema": "expanse_tracking_python"}
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("expanse_tracking_python.users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    category_id = Column(
        Integer, ForeignKey("expanse_tracking_python.categories.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    amount = Column(Float,nullable=False)
    description = Column(Text,nullable=True)
    date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    
    