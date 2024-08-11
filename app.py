# app.py
from flask import Flask, render_template, request, jsonify, url_for, Response, Blueprint
import mysql.connector
from mysql.connector import Error
import joblib
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import numpy as np
from facturas.registrar_facturas import facturas_bp

#importar librerias para el login y signup
from flask_bcrypt import Bcrypt


app = Flask(__name__, template_folder="templates")
#codigo para contraseña
app.config['SECRET_KEY'] = '1234'
bcrypt = Bcrypt(app)

app.register_blueprint(facturas_bp, url_prefix='/facturas')


#conexion a bd
def db_connect():
    try:
        connection = mysql.connector.connect(
            #bd dani
            user='root',
            password='Altima_2800',
            host='localhost',
            database='boomai',
            port='3307'
            #bd ivan
            #user='virtualbox1',
            #password='Altima_2800',
            #host='172.29.193.211',
            #database='boomai',
            #port='3306
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None


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

#Ruta para crear una cuenta

@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"message": "Content-Type debe ser 'application/json'", "success": False}), 200

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Faltan datos", "success": False}), 200

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    connection = db_connect()
    if connection is None:
        return jsonify({"message": "No se pudo conectar a la base de datos", "success": False}), 200

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO usuario (usuario, email, contraseña) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, email, hashed_password))
        connection.commit()
        return jsonify({"message": "Usuario registrado exitosamente", "success": True}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 200
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

##Ruta para iniciar sesion


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Content-Type debe ser 'application/json'", "success": False}), 200

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Faltan datos", "success": False}), 200

    connection = db_connect()
    if connection is None:
        return jsonify({"message": "No se pudo conectar a la base de datos", "success": False}), 200

    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM usuario WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.check_password_hash(user[3], password):  # user[3] es la columna de la contraseña
            return jsonify({"message": "Inicio de sesión exitoso", "success": True}), 200
        else:
            return jsonify({"message": "Credenciales incorrectas", "success": False}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 200
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
   app.run(debug=True)