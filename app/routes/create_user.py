from sqlalchemy.orm import Session
from app.models.user import User
from app.models.userType import UserType
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import User as UserSchema
import bcrypt
from fastapi import HTTPException
from sqlalchemy.future import select


async def create_user(db:AsyncSession , user: UserSchema):

    
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    result = await db.execute(select(UserType).where(UserType.name == 'usuario'))
    roli = result.scalars().first()

    db_user = User(  
        name=user.name,
        email=user.email,
        password=hashed_password,
        weight=user.weight,
        gender=user.gender,
        age=user.age,
        id_user_type=roli.id 
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user