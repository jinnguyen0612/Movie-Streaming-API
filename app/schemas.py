"""
Create Schemas
Author: jinnguyen0612
Email: hoangha0612.work@gmail.com
"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    role: int
    class Config:
        orm_mode = True
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
