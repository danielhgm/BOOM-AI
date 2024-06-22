from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        # Procesar la factura y devolver resultados
        return "File uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True)