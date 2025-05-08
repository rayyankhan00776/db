from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class Role(str, Enum):
    creator = "creator"
    consumer = "consumer"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[Role] = Role.consumer  # Use enum here
