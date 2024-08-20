from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class Report(Base):
    __tablename__ = "reports"
    __table_args__ = {"schema": "expanse_tracking_python"}

    # Primary key for the Report table
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    
    # Foreign key linking to the User table
    user_id = Column(
        Integer, ForeignKey("expanse_tracking_python.users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    
    # Name of the report
    name = Column(String(20), nullable=False)
    
    # Description of the report
    description = Column(String(255))
    
    # Start date of the report period
    start_date = Column(DateTime(timezone=True))
    
    # End date of the report period
    end_date = Column(DateTime(timezone=True))
    
    # Timestamps for record creation and updates
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to the User model
    user = relationship("User", back_populates="reports")
