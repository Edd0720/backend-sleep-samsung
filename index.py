from typing import Union
from app.schemas.user import UserBase
from fastapi import FastAPI,Depends, Request
from app.services .auth import AuthService
from app.db.database import get_db, engine
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.routes import auth
from app.routes.create_user import create_user
from app.db.database import get_db 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from modelo import cargar_modelo, predecir
from app.services.sleepService import SleepService
import numpy as np
import pandas as pd
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
async def predict(payload: SleepData):
    try:
        # Cargar el modelo
        model = cargar_modelo()
        if model is None:
            return {"error": "No se pudo cargar el modelo"}

        # Crear el DataFrame de entrada con los nombres correctos
        input_data = pd.DataFrame([[
            float(payload.age),
            float(payload.gender),
            float(payload.sleep_duration),
            float(payload.sleep_rem),
            float(payload.sleep_deep),
            float(payload.sleep_light),
            float(payload.awakenings),
            float(payload.caffeine),
            float(payload.alcohol),
            float(payload.smoking_status),
            float(payload.exercise_frequency)
        ]], columns=[
            "Age", "Gender", "Sleep_duration", "REM_sleep_percentage", "Deep_sleep_percentage",
            "Light_sleep_percentage", "Awakenings", "Caffeine_consumption", "Alcohol_consumption", 
            "Smoking_status", "Exercise_frequency"
        ])

        # Imprimir datos de entrada
        print("Datos de entrada para la predicción:", input_data)

        # Hacer la predicción directamente con el DataFrame
        prediction = model.predict(input_data)[0]
        print("Predicción:", prediction)

        return {"prediction": prediction}

    except Exception as e:
        print(f"Error en la predicción: {str(e)}")
        return {"error": str(e)}
    

#ruta para registrar los datos del sueño
@app.post("/sleep/register")
async def register_sleep(sleep_data:SleepData,db:AsyncSession=Depends(get_db)):
    sleep_service = SleepService(db=db)
    sleep = await sleep_service.create_sleep_data(sleep_data=sleep_data)
    return sleep
    
   


#ruta para crear un usuario
@app.post("/auth/register")
async def create_register(user_data:UserBase,db:AsyncSession=Depends(get_db)):
    user = await create_user(db=db, user=user_data)
    return user
    

