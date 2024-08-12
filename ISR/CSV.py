import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import Ridge
import joblib

# Cargar los datos
df = pd.read_csv('../data/datos_impuestos.csv')

# Ejemplo de columnas en el dataset
# df.head()
# | ingresos | deducciones | creditos_fiscales | tipo_contribuyente | impuesto_a_pagar |
# | -------- | ----------- | ----------------- | ------------------ | ---------------- |

# Separar características y la variable objetivo
X = df.drop('impuesto_a_pagar', axis=1)
y = df['impuesto_a_pagar']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocesamiento de datos
numeric_features = ['ingresos', 'deducciones', 'creditos_fiscales']
categorical_features = ['tipo_contribuyente']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),  # Añadir interacciones polinómicas
    ('pca', PCA(n_components=5))  # Reducción de dimensionalidad si es necesario
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Selección de características
feature_selector = SelectKBest(score_func=f_regression, k='all')

# Modelos individuales para Stacking
base_models = [
    ('rf', RandomForestRegressor(random_state=42)),
    ('gbr', GradientBoostingRegressor(random_state=42)),
    ('ridge', Ridge(alpha=1.0))
]

# Ensamblaje con Stacking
stacking_model = StackingRegressor(estimators=base_models, final_estimator=Ridge())

# Crear el pipeline completo
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('feature_selection', feature_selector),
    ('model', stacking_model)
])

# Definir una grid de hiperparámetros
param_grid = {
    'model_ridge_alpha': [0.1, 1.0, 10.0],
    'model_rf_n_estimators': [100, 200],
    'model_rf_max_depth': [10, 20],
    'model_gbr_n_estimators': [100, 200],
    'model_gbr_learning_rate': [0.01, 0.1, 0.2]
}

# K-Fold cross-validation
kf = KFold(n_splits=10, shuffle=True, random_state=42)

# GridSearchCV con validación cruzada
grid_search = GridSearchCV(pipeline, param_grid, cv=kf, scoring='neg_mean_squared_error', n_jobs=-1)

# Entrenar el modelo
grid_search.fit(X_train, y_train)

# Mejor modelo encontrado
best_model = grid_search.best_estimator_

# Evaluar el modelo en el conjunto de prueba
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Best Parameters: {grid_search.best_params_}")
print(f"Mean Squared Error on Test Set: {mse}")
print(f"Mean Absolute Error on Test Set: {mae}")
print(f"R2 Score on Test Set: {r2}")

# Guardar el modelo entrenado
joblib.dump(best_model, 'modelo_calculo_impuestos_avanzado.pkl')

# Si es necesario, se pueden analizar las características más importantes
importances = best_model.named_steps['model'].final_estimator_.coef_
features = np.array(X.columns)
indices = np.argsort(importances)

print("Feature importances:")
for i in indices:
    print(f"{features[i]}: {importances[i]}")