# app.py
from flask import Flask, request, jsonify
import joblib
from datetime import datetime

app = Flask(__name__)
inventory_model = joblib.load('models/inventory_model.pkl')

@app.route('/predict_inventory', methods=['POST'])
def predict_inventory():
    data = request.json
    product_id = data['product_id']
    units_in_stock = data['units_in_stock']
    date = datetime.strptime(data['date'], '%Y-%m-%d')
    
    # Crear características adicionales
    day_of_week = date.weekday()
    month = date.month
    
    features = [[product_id, units_in_stock, day_of_week, month]]
    
    # Escalar las características
    scaler = joblib.load('models/scaler.pkl')
    features_scaled = scaler.transform(features)
    
    prediction = inventory_model.predict(features_scaled)
    return jsonify({'predicted_units_sold': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)