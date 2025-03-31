from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sleep import SleepData
from app.models.smartwatch import SmartWatch
from app.models.data import DataApp
from app.models.dailyReport import DailyReport
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import date
from sqlalchemy.sql.expression import and_

class SleepService:
  def __init__(self,db:AsyncSession):
    self.db = db
    
  async def create_sleep_data(self,sleep_data:SleepData):
    #crean el registro de datos del smartwach
    db_sleep = SmartWatch(
      sleep_duration=sleep_data.sleep_duration,
      rem_sleep_cycle=sleep_data.sleep_rem,
      deep_sleep_cycle=sleep_data.sleep_deep,
      light_sleep_cycle=sleep_data.sleep_light,
      bedtime_hour=sleep_data.bedtime,
      awakenings= sleep_data.awakenings,
      wakeup_hour=sleep_data.wakeup
    )
    self.db.add(db_sleep)
    await self.db.commit()
    await self.db.refresh(db_sleep)
    
    #crea el registro de datos restantes de la app
    
    db_data = DataApp(
      smoking_status=sleep_data.smoking_status,
      caffeine_consumption=sleep_data.caffeine,
      excercise_frecuency=sleep_data.excercise,
      alcohol_consumption=sleep_data.alcohol
    )
    self.db.add(db_data)
    await self.db.commit()
    await self.db.refresh(db_data)
    
    #datos de la tabla intermedia 
    db_daily_report = DailyReport(
      id_user=sleep_data.user_id,
      id_data=db_data.id,
      id_smartwatch=db_sleep.id,
      date_daily=date.today()
    )
    self.db.add(db_daily_report)
    await self.db.commit()
    await self.db.refresh(db_daily_report)
    return db_daily_report
  
  async def get_sleep_data(self,user_id:int):
    result = await self.db.execute(
      select(DailyReport)
        .where(and_(
          DailyReport.date_daily == date.today(),
          DailyReport.id_user == user_id
        ))
        .options(
          selectinload(DailyReport.smart_watch),
          selectinload(DailyReport.data_app)
        )
    )
    return result.scalar_one_or_none()
  

    
    