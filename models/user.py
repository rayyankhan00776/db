# models/user.py (updated)
from sqlalchemy import TEXT, VARCHAR, Column, LargeBinary, DateTime
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100), unique=True)
    password = Column(LargeBinary)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    media = relationship("Media", back_populates="user")
    likes = relationship("Like", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")