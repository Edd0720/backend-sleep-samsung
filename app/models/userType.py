from app.db.database import Base
from sqlalchemy.orm import relationship,mapped_column,Mapped
from sqlalchemy import String
from typing import List
class UserType(Base):
  __tablename__ = 'user_type'
  id:Mapped[int] = mapped_column(primary_key=True,index=True)
  name:Mapped[str] = mapped_column(String(100),nullable=False)
  users:Mapped[List['User']] = relationship(back_populates='user_type',cascade='all, delete-orphan')