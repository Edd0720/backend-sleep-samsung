from typing import Union
from app.schemas.user import UserBase
from fastapi import FastAPI,Depends
from app.services .auth import AuthService
from app.db.database import session_local
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
app = FastAPI()

async def get_db()->AsyncSession:
    async with session_local() as session:
        yield session


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/auth/register")
async def create_user(user_data:UserBase,db:AsyncSession=Depends(get_db)):
    userService = AuthService(db=db)
    user = await userService.create_user(user=user_data,userModel=User)
    return user
    

