from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import user
from app.models import user as userModel
class AuthService:
  def __init__(self,db:AsyncSession):
    self.db = db
    
  async def create_user(self,user:user.UserBase,userModel:userModel.User):
    db_user = userModel(
      email=user.email,
      password=user.password,
      age=user.age,
      gender=user.gender,
      id_user_type = 1,
    )
    self.db.add(db_user)
    await self.db.commit()
    await self.db.refresh(db_user)
    return db_user