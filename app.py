# app.py
from flask import Flask, render_template, request, jsonify, url_for, Response, Blueprint
import mysql.connector
from mysql.connector import Error
import joblib
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import numpy as np
from flask_socketio import SocketIO
from facturas.registrar_facturas import facturas_bp


app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app)

app.register_blueprint(facturas_bp, url_prefix='/facturas')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/tuempresa')
def tuempresa():
    return render_template('tuempresa.html')

@app.route('/estancia')
def estancia():
    return render_template('estancia.html')

if __name__ == '__main__':
    app.run(debug=True)