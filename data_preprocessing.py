import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data(file_path):
    # Cargar datos
    data = pd.read_csv(file_path, parse_dates=['date'])
    
    # Crear características adicionales
    data['day_of_week'] = data['date'].dt.dayofweek
    data['month'] = data['date'].dt.month
    
    # Seleccionar características y etiquetas
    X = data[['product_id', 'units_in_stock', 'day_of_week', 'month']]
    y = data['units_sold']
    
    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Escalar las características
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test