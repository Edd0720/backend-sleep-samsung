
from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
  email:EmailStr
  name:str
  password:str
  age:str
  gender:bool
  
class User(UserBase):
    id: int
    id_user_type: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str