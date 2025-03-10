
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

datset = pd.read_csv('SSD_V7.csv')

datset.rename(columns = {'Wakeup time':'Wakeup_time', 'Sleep duration':'Sleep_duration',"Sleep efficiency":"Sleep_efficiency",
                     "REM sleep percentage":"REM_sleep_percentage","Deep sleep percentage":"Deep_sleep_percentage",
                     "Light sleep percentage":"Light_sleep_percentage","Caffeine consumption":"Caffeine_consumption",
                     "Alcohol consumption":"Alcohol_consumption","Smoking status":"Smoking_status","Exercise frequency":"Exercise_frequency"}, inplace = True)

datset.head(5)

datset.head(5)

le = LabelEncoder()

norm_datset = datset.drop(['Bedtime', 'Wakeup_time', 'ID','Calidad_sueño'], axis=1)

norm_datset['Gender'] = le.fit_transform(norm_datset['Gender'])
norm_datset['Smoking_status'] = le.fit_transform(norm_datset['Smoking_status'])

norm_datset.dtypes

norm_datset['Gender'] = norm_datset['Gender'].astype('category')
norm_datset['Smoking_status'] = norm_datset['Smoking_status'].astype('category')

"""# Entrenamiento del modelo con 453 datos"""

norm_datset.corr()

X = norm_datset.drop(['Sleep_efficiency'], axis=1) #variables independientes
y = norm_datset['Sleep_efficiency'] #variable dependiente

#Division de los datos en 30% prueba y 70% entrenamiento

def cargar_modelo():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

    rfr = RandomForestRegressor(random_state=1234)
    # Aquí puedes definir tu modelo entrenado
    model = RandomForestRegressor(n_estimators=300,max_depth=20,min_samples_split=5,min_samples_leaf=2)
    # Predecir en el conjunto de prueba
    model.fit(X_train, y_train)
    Y_pred = model.predict(X_test)
    return model

# Función para hacer predicciones
def predecir(model, input_data):
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)
    return prediction[0]
