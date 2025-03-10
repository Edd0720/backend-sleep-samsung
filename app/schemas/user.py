
from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
  email:EmailStr
  name:str
  password:str
  age:str
  gender:bool
  
class User(UserBase):
  id:int