from models.base import Base
from sqlalchemy import TEXT, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(TEXT, primary_key=True)
    media_id = Column(TEXT, ForeignKey("media.id"), nullable=False)
    user_id = Column(TEXT, ForeignKey("users.id"), nullable=False)
    text = Column(TEXT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    media = relationship("Media", back_populates="comments")
    user = relationship("User", back_populates="comments")