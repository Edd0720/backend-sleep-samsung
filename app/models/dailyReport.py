from app.db.database import Base
from sqlalchemy import ForeignKey,Date
from sqlalchemy.orm import relationship,mapped_column,Mapped
from datetime import date
class DailyReport(Base):
  __tablename__ = 'daily_report'
  id:Mapped[int] = mapped_column(primary_key=True,index=True,autoincrement='auto')
  id_user:Mapped[int]= mapped_column(ForeignKey('user.id'))
  id_data:Mapped[int]= mapped_column(ForeignKey('data_app.id'))
  id_smartwatch:Mapped[int] =  mapped_column(ForeignKey('smartwatch.id'))
  date_daily:Mapped[date] = mapped_column(Date,nullable=True)
  
  user:Mapped['User'] = relationship(back_populates='daily_report')
  data_app:Mapped['DataApp'] = relationship(back_populates='daily_report')
  smart_watch:Mapped['SmartWatch']= relationship(back_populates='daily_report')
  

