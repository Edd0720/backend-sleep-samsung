from typing import Union
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from modelo import cargar_modelo, predecir
import numpy as np


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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

# Crear la aplicación FastAPI
app = FastAPI()

# Montar la carpeta static para servir archivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta para servir el archivo HTML
@app.get("/index", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r",encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

# Ruta para hacer predicciones
@app.post("/predict/")
def predict(data: InputData):
    try:
        # Convertir los datos de entrada a un array
        input_data = [
            data.Age,
            data.Gender,
            data.Sleep_duration,
            data.REM_sleep_percentage,
            data.Deep_sleep_percentage,
            data.Light_sleep_percentage,
            data.Awakenings,
            data.Caffeine_consumption,
            data.Alcohol_consumption,
            data.Smoking_status,
            data.Exercise_frequency
        ]

        # Hacer la predicción
        prediction = predecir(model, input_data)
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}