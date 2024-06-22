from flask import Flask, request, jsonify, render_template
from PIL import Image
import pytesseract
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

# Inicialización del modelo de clasificación de gastos
invoices = ["Compra de suministros de oficina", "Pago de servicios de internet", "Compra de equipos de computo"]
categories = ["Office Supplies", "Internet Services", "Computer Equipment"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(invoices)
clf_expense = MultinomialNB()
clf_expense.fit(X, categories)

# Inicialización del modelo de detección de fraudes
amounts = [120, 80, 50, 30, 10000]
amounts = pd.DataFrame(amounts, columns=['amount'])
clf_fraud = IsolationForest(contamination=0.1)
clf_fraud.fit(amounts)

def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    print("Texto extraído:", text)  # Imprime el texto extraído para depurar
    return text

def parse_invoice(text):
    data = {}
    # Corrección en las expresiones regulares para capturar correctamente los datos
    match_date = re.search(r'Fecha:\s*(\d{2}/\d{2}/\d{4})', text)
    if match_date:
        data['date'] = match_date.group(1)
    else:
        data['date'] = "Fecha no encontrada"  # Manejo de errores

    match_total = re.search(r'Total:\s+\$?(\d+\.\d{2})', text)
    if match_total:
        data['total'] = match_total.group(1)
    else:
        data['total'] = "Total no encontrado"  # Manejo de errores

    match_description = re.search(r'Descripción:\s+(.*)', text)
    if match_description:
        data['description'] = match_description.group(1)
    else:
        data['description'] = "Descripción no encontrada"  # Manejo de errores

    return data

def classify_expense(description):
    X_new = vectorizer.transform([description])
    return clf_expense.predict(X_new)[0]

def detect_fraud(amount):
    return clf_fraud.predict([[amount]])[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path = f'uploads/{file.filename}'
        file.save(file_path)
        text = extract_text(file_path)
        
        # Debugging prints
        print("Texto extraído:", text)
        
        data = parse_invoice(text)
        print("Datos parseados:", data)
        
        data['category'] = classify_expense(data['description'])
        data['fraud'] = "Yes" if detect_fraud(float(data['total'])) == -1 else "No"
        print("Datos finales:", data)
        
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)