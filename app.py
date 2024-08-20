# app.py
from flask import Flask, render_template, request, jsonify, url_for, Response, Blueprint, session, redirect
#from flask import redirect_request(req, fp, code, msg, hdrs, newurl)
import mysql.connector
from mysql.connector import Error
import joblib
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import numpy as np
from facturas.registrar_facturas import facturas_bp
from facturas.registrar_proveedores import proveedores_bp
from facturas.registrar_gastos import gastos_bp
from flask_bcrypt import Bcrypt

#from flask_oauthlib.client import OAuth --> Este quedo con # ya que era una funcion con problema en otras versiones con otras librerias
#(eliminar esta libreria flask_oauthlib")
import os

app = Flask(__name__, template_folder="templates")
bcrypt = Bcrypt(app)
app.secret_key = '1234' #No eliminar, es para que pueda funcionar el login

app.register_blueprint(facturas_bp, url_prefix='/facturas')
app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
app.register_blueprint(gastos_bp, url_prefix='/gastos')

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
            #port='3306'
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None


@app.route('/')
def index_sesion_no_iniciada():
    return render_template('index_sesion_no_iniciada.html')

@app.route('/index_sesion_iniciada')
def index_sesion_iniciada():
    return render_template('index_sesion_iniciada.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/tuempresa')
def tuempresa():
    return render_template('tuempresa.html')

@app.route('/estancia')
def estancia():
    return render_template('estancia.html')

#Ruta para dashboard chatgpt

@app.route('/plantilla_dashboard')
def plantilla_dashboard():
    return render_template('servicios/plantilla_dashboard.html')

#Ruta para ISR

@app.route('/ISR')
def ISR():
    return render_template('ISR.html')

#Ruta para crear una cuenta

@app.route('/register', methods=['POST','GET'])
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
        return jsonify({"message": "Content-Type debe ser 'application/json'", "success": False}), 201

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
            session['user_id'] = user[0]  # Almacena el ID del usuario en la sesión
            # Imprimir en la terminal
            print(f"Usuario inició sesión con: ID={user[0]}, Usuario={user[1]}, Correo={user[2]}")  # Ajusta los índices según tu esquema
            return jsonify({"message": "Inicio de sesión exitoso", "success": True, "redirect_url": url_for('dashboard')})
        else:
            return jsonify({"message": "Credenciales incorrectas", "success": False}), 210
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 211
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# recuperar user_id
def verify_user(username, password):
    connection = db_connect()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuario WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()  # Esto devuelve un diccionario con el id del usuario
        connection.close()
        return user['id'] if user else None
    return None

#ruta para mantener el login
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Realizar operaciones que requieran autenticación
        return render_template('index_sesion_iniciada.html')
    else:
        return redirect(url_for('index_sesion_no_iniciada'))  # Redirige a una página de inicio de sesión si el usuario no está autenticado


if __name__ == '__main__':
   app.run(debug=True)