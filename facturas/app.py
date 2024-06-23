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
DATABASE_URL = 'sqlite:///facturas.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Definición del modelo de la base de datos
class Factura(Base):
    __tablename__ = 'facturas'
    id = Column(Integer, primary_key=True)
    fecha = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    importe = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    emisor = Column(String, nullable=False)
    folio = Column(String, nullable=False)
    beneficiario = Column(String, nullable=False)

Base.metadata.create_all(engine)

# Ruta para la página de inicio
@app.route('/')
def index():
    try:
        facturas = session.query(Factura).all()
    except SQLAlchemyError as e:
        return str(e)
    return render_template('index.html', facturas=facturas)

# Ruta para borrar todos los registros de la base de datos
@app.route('/delete_all', methods=['POST'])
def delete_all():
    try:
        session.query(Factura).delete()
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        return str(e)
    return redirect(url_for('index'))

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

            # Separar texto por cada factura detectada
            facturas_texto = separar_facturas(text)

            # Procesar cada factura detectada
            for factura_texto in facturas_texto:
                process_text(factura_texto)

            return redirect(url_for('index'))
        except Exception as e:
            return str(e)

def process_text(text):
    fecha = descripcion = importe = hora = emisor = folio = beneficiario = "no especifica"

    lines = text.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            if key == 'fecha':
                fecha = value
            elif key == 'descripción' or key == 'motivo':
                descripcion = value
            elif key == 'importe total' or key == 'cantidad total':
                importe = value
            elif key == 'hora':
                hora = value
            elif key == 'nombre del emisor':
                emisor = value
            elif key == 'folio':
                folio = value
            elif key == 'beneficiario' or key == 'receptor':
                beneficiario = value

    try:
        factura = Factura(fecha=fecha, descripcion=descripcion, importe=importe, hora=hora,
                          emisor=emisor, folio=folio, beneficiario=beneficiario)
        session.add(factura)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e

def separar_facturas(text):
    # Separar el texto en partes correspondientes a cada factura
    facturas_texto = []
    lines = text.split('\n')
    factura_actual = []
    for line in lines:
        if ':' in line:
            factura_actual.append(line)
        elif factura_actual:
            facturas_texto.append('\n'.join(factura_actual))
            factura_actual = []
    if factura_actual:
        facturas_texto.append('\n'.join(factura_actual))
    return facturas_texto

if __name__ == '__main__':
    app.run(debug=True)
