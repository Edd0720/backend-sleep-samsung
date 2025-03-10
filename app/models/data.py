from sqlalchemy.orm import relationship,mapped_column,Mapped
from app.db.database import Base
from typing import List
class DataApp(Base):
  __tablename__ = 'data_app'
  id:Mapped[int] = mapped_column(primary_key=True,index=True,autoincrement='auto')
  smoking_status:Mapped[bool] = mapped_column(nullable=True)
  caffeine_consumption:Mapped[int] = mapped_column(nullable=True)
  excercise_frecuency:Mapped[int] = mapped_column(nullable=True)
  alcohol_consumption:Mapped[int] = mapped_column(nullable=True)
  daily_report:Mapped[List['DailyReport']]= relationship(back_populates='data_app')
