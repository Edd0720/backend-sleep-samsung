
from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
  email:EmailStr
  name:str
  password:str
  age:str
  gender:bool
  weight:float
  
class User(UserBase):
  id:int
  name:str
  email:EmailStr

  class Config:
    orm_mode = True