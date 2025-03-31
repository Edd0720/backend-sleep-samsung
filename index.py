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

@app.get("/ping")
async def ping():
   return {"message": "pong!"}
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Ruta para hacer predicciones
@app.post("/predict/")
async def predict(sleep_data:SleepData,db:AsyncSession=Depends(get_db)):
    try:
        sleep_service = SleepService(db=db)
        user_service = AuthService(db=db)
        sleep = await sleep_service.create_sleep_data(sleep_data=sleep_data)
        data_user = await user_service.get_data_user(user_id=sleep.id_user)
        # Cargar el modelo
        model = cargar_modelo()
        # Convertir los datos de entrada a un array
        input_data = [
            data_user.age,
            data_user.gender,
            sleep.smart_watch.rem_sleep_cycle,
            sleep.smart_watch.deep_sleep_cycle,
            sleep.smart_watch.light_sleep_cycle,
            sleep.smart_watch.awakenings,
            sleep.data_app.caffeine_consumption,
            sleep.data_app.alcohol_consumption,
            sleep.data_app.smoking_status,
            sleep.data_app.excercise_frecuency,
            
        ]
        # Hacer la predicción
        prediction = predecir(model, input_data)
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}
    


#ruta para crear un usuario
@app.post("/auth/register")
async def create_user(user_data:UserBase,db:AsyncSession=Depends(get_db)):
    userService = AuthService(db=db)
    user = await userService.create_user(user=user_data,userModel=User)
    return user
    