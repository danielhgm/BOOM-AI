# train_inventory_model.py
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
from data_preprocessing import load_and_preprocess_data

# Cargar y preprocesar datos
X_train, X_test, y_train, y_test = load_and_preprocess_data('data/inventory_data.csv')

# Entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Guardar el modelo
joblib.dump(model, 'models/inventory_model.pkl')

joblib.dump(scaler, 'models/scaler.pkl')