from typing import Union
from app.schemas.user import UserBase
from fastapi import FastAPI,Depends, Request
from app.services .auth import AuthService
from app.db.database import session_local
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.routes import auth
from app.db.database import get_db 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from modelo import cargar_modelo, predecir
from app.services.sleepService import SleepService
import numpy as np
from app.schemas.sleep import SleepData
app = FastAPI()
app.include_router(auth.router)
import numpy
print(numpy.__file__)


# Montar la carpeta static para servir archivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta para servir el archivo HTML
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read())

# Ruta para hacer predicciones
@app.post("/predict/")
async def predict(user_id:int,db:AsyncSession=Depends(get_db)):
    try:
        # Cargar el modelo
        model = cargar_modelo()
        sleep_service= SleepService(db=db)
        user_service = AuthService(db=db)
        data_sleep = await sleep_service.get_sleep_data(user_id=user_id)
        data_user = await user_service.get_data_user(user_id=user_id)
        # Convertir los datos de entrada a un array
        input_data = [
            data_user.age,
            data_user.gender,
            data_sleep.smart_watch.rem_sleep_cycle,
            data_sleep.smart_watch.deep_sleep_cycle,
            data_sleep.smart_watch.light_sleep_cycle,
            data_sleep.smart_watch.awakenings,
            data_sleep.data_app.caffeine_consumption,
            data_sleep.data_app.alcohol_consumption,
            data_sleep.data_app.smoking_status,
            data_sleep.data_app.excercise_frecuency,
            
        ]
        # Hacer la predicción
        prediction = predecir(model, input_data)
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}
    

#ruta para registrar los datos del sueño
@app.post("/sleep/register")
async def register_sleep(sleep_data:SleepData,db:AsyncSession=Depends(get_db)):
    sleep_service = SleepService(db=db)
    sleep = await sleep_service.create_sleep_data(sleep_data=sleep_data)
    return sleep
    
   


#ruta para crear un usuario
@app.post("/auth/register")
async def create_user(user_data:UserBase,db:AsyncSession=Depends(get_db)):
    userService = AuthService(db=db)
    user = await userService.create_user(user=user_data,userModel=User)
    return user
    

