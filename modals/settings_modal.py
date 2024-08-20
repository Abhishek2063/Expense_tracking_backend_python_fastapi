from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class ReminderSetting(Base):
    __tablename__ = "reminder_settings"
    __table_args__ = {"schema": "expanse_tracking_python"}
    
    # Primary key for the ReminderSettings table
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    
    # Foreign key to the User table
    user_id = Column(
        Integer, ForeignKey("expanse_tracking_python.users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    
    # Budget limit for reminders
    budget_limit = Column(Float, nullable=False)
    
    # Timestamps for record creation and updates
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    
    # Relationship to the User table
    user = relationship("User", back_populates="reminder_settings")
