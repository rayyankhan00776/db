from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, LargeBinary

class UserLogin(BaseModel):
    email: EmailStr
    password = Column(LargeBinary, nullable=False)
