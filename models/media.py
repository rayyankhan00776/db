# models/media.py
from models.base import Base
from sqlalchemy import TEXT, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import String
from datetime import datetime

class Media(Base):
    __tablename__ = 'media'
    
    id = Column(TEXT, primary_key=True)
    media_url = Column(String, nullable=True)
    public_id = Column(TEXT, nullable=False)  # Cloudinary public ID
    description = Column(TEXT)
    user_id = Column(TEXT, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="media")
    likes = relationship("Like", back_populates="media", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="media", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="media", cascade="all, delete-orphan")