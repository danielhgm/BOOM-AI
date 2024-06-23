import os
import pytesseract
import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = 'sqlite:///facturas_4pm_primitivo.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Definición del modelo de la base de datos
class Factura(Base):
    __tablename__ = 'facturas_4pm_primitivo'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    dato = Column(String, nullable=False)

Base.metadata.create_all(engine)

# Ruta para la página de inicio
@app.route('/')
def index():
    try:
        facturas = session.query(Factura).all()
    except SQLAlchemyError as e:
        return str(e)
    return render_template('index_4pm_primitivo.html', facturas=facturas)

# Ruta para subir y procesar la factura
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        try:
            # Abrir imagen y aplicar preprocesamiento con OpenCV
            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
            # Convertir imagen preprocesada de OpenCV a formato PIL
            image_pil = Image.fromarray(gray)
            
            # Aplicar OCR con Tesseract a la imagen preprocesada
            custom_config = r'--oem 3 --psm 6 -l spa'
            text = pytesseract.image_to_string(image_pil, config=custom_config)
            
            process_text(text)
            return redirect(url_for('index'))
        except Exception as e:
            return str(e)

def process_text(text):
    lines = text.split('\n')
    for line in lines:
        if ':' in line:
            titulo, dato = line.split(':', 1)
            titulo = titulo.strip()
            dato = dato.strip()
            if titulo and dato:
                factura = Factura(titulo=titulo, dato=dato)
                session.add(factura)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e

if __name__ == '__main__':
    app.run(debug=True)
