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
import numpy as np
app = FastAPI()
app.include_router(auth.router)
import numpy
print(numpy.__file__)


# Cargar el modelo
model = cargar_modelo()

# Definir la estructura de los datos de entrada
class InputData(BaseModel):
    Age: int
    Gender: int  # 0 para Femenino, 1 para Masculino
    Sleep_duration: float
    REM_sleep_percentage: float
    Deep_sleep_percentage: float
    Light_sleep_percentage: float
    Awakenings: int
    Caffeine_consumption: int
    Alcohol_consumption: int
    Smoking_status: int  # 0 para No, 1 para Sí
    Exercise_frequency: int


# Montar la carpeta static para servir archivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta para servir el archivo HTML
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.get("/ping")
async def ping():
   return {"message": "pong!"}
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/auth/register")
async def create_user(user_data:UserBase,db:AsyncSession=Depends(get_db)):
    userService = AuthService(db=db)
    user = await userService.create_user(user=user_data,userModel=User)
    return user
    
# Definimos una ruta para realizar predicciones usando datos de entrada.
@app.post("/predict/")  
def predict(data: InputData):  # La función recibe un objeto InputData con los datos del usuario.
    try:
        # Convertimos los datos de entrada en un array para alimentar al modelo de predicción.
        input_data = [  
            data.Age,  # Edad del usuario.
            data.Gender,  # Género del usuario.
            data.Sleep_duration,  # Duración del sueño.
            data.REM_sleep_percentage,  # Porcentaje de sueño REM.
            data.Deep_sleep_percentage,  # Porcentaje de sueño profundo.
            data.Light_sleep_percentage,  # Porcentaje de sueño ligero.
            data.Awakenings,  # Número de despertares.
            data.Caffeine_consumption,  # Consumo de cafeína.
            data.Alcohol_consumption,  # Consumo de alcohol.
            data.Smoking_status,  # Estado de fumador (no definido en la clase InputData).
            data.Exercise_frequency  # Frecuencia de ejercicio (no definido en la clase InputData).
        ]

        # Hacemos la predicción utilizando el modelo entrenado y los datos de entrada.
        prediction = predecir(model, input_data)  
        return {"prediction": prediction}  # Retornamos la predicción como una respuesta JSON.
    except Exception as e:  # Manejamos cualquier error que ocurra durante la ejecución.
        return {"error": str(e)}  # Retornamos el error como respuesta JSON.