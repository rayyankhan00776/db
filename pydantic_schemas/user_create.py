from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, LargeBinary

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password = Column(LargeBinary, nullable=False)
