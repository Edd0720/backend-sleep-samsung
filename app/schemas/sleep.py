from pydantic import BaseModel

# Definir el esquema del cuerpo de la solicitud
class SleepData(BaseModel):
    user_id: int
    gender: int
    age: int
    sleep_duration: float
    sleep_rem: int
    sleep_deep: int
    sleep_light: int
    awakenings: int
    caffeine: int
    alcohol: int
    smoking_status: bool
    exercise_frequency: int
    bedtime: float
    wakeup: float