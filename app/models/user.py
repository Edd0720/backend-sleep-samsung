from app.db.database import Base
from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import relationship,mapped_column,Mapped
from typing import List
class User(Base):
  __tablename__ = 'user'
  id:Mapped[int] = mapped_column(primary_key=True,index=True)
  email:Mapped[str] = mapped_column(String(100),nullable=False)
  password:Mapped[str] = mapped_column(String(255),nullable=False)
  name:Mapped[str] = mapped_column(String(100),nullable=False)
  age:Mapped[int] = mapped_column(nullable=False)
  gender:Mapped[bool]= mapped_column(nullable=False)
  id_user_type:Mapped[int] = mapped_column(ForeignKey('user_type.id'))
  user_type:Mapped['UserType'] = relationship('UserType',back_populates='user')
  daily_report:Mapped[List['DailyReport']] = relationship(back_populates='user',cascade='all, delete-orphan')