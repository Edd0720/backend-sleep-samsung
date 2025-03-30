from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserBase
from app.models.user import User
from sqlalchemy.future import select
class AuthService:
  def __init__(self,db:AsyncSession):
    self.db = db
    
  async def create_user(self,user:UserBase):
    db_user = User(
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
  
  async def get_data_user(self,user_id):
    result = await self.db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()