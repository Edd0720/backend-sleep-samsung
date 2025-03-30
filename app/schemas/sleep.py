from pydantic import BaseModel

class SleepData(BaseModel):
  user_id:int
  sleep_duration:float
  sleep_rem:float
  sleep_deep:float
  sleep_light:float
  bedtime:float
  awakenings:int
  wakeup:float
  smoking_status:bool
  caffeine:int
  excercise:int
  alcohol:int