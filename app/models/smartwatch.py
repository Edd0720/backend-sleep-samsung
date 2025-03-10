from app.db.database import Base
from sqlalchemy.orm import relationship,mapped_column,Mapped
from typing import List
class SmartWatch(Base):
  __tablename__ = 'smartwatch'
  id:Mapped[int] = mapped_column(primary_key=True,index=True,autoincrement='auto')
  sleep_duration:Mapped[float] = mapped_column(nullable=False)
  rem_sleep_cycle:Mapped[float] = mapped_column(nullable=False)
  deep_sleep_cycle:Mapped[float] = mapped_column(nullable=False)
  light_sleep_cycle:Mapped[float] = mapped_column(nullable=False)
  bedtime_hour:Mapped[float]= mapped_column(nullable=False)
  awakenings:Mapped[int]= mapped_column(nullable=False)
  wakeup_hour:Mapped[float]= mapped_column(nullable=False)
  daily_report:Mapped[List['DailyReport']] = relationship(back_populates='smart_watch')