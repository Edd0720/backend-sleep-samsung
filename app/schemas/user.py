from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str
    password: str
    age: int
    gender: bool
    weight: float
    id_user_type: Optional[int] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  

class UserLogin(BaseModel):
    email: EmailStr
    password: str
