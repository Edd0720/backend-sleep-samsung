from sqlalchemy.orm import Session
from models import user
from schemas import user
import bcrypt

def create_user(db: Session, user: user.UserBase):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    db_user = user(name=user.name, 
                   email=user.email, 
                   hashed_password=hashed_password, 
                   weight=user.weight,
                   gender=user.gender,
                   age=user.age,
                   id_user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user