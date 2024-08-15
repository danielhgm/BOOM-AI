# app.py
from flask import Flask, render_template, request, jsonify, url_for, Response, Blueprint, session, redirect
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
#importacion de librerias de google
import google.auth.transport.requests
import google.oauth2.id_token
#from flask_oauthlib.client import OAuth --> Este quedo con # ya que era una funcion con problema en otras versiones con otras librerias
#(eliminar esta libreria flask_oauthlib")
from authlib.integrations.flask_client import OAuth #este es el perron
import os

app = Flask(__name__, template_folder="templates")
#codigo para contraseña
bcrypt = Bcrypt(app)
#codigo para tokens relacionados con GOOGLE CLOUD SERVICES para inicio o creacion de cuenta con google
#(como es servidor prueba solo pueden crearse cuenta o acceder degovan...@gmail.com y competitivogral756@gmail.com)
#Una vez ya teniendo el dominio real ya podran acceder hasta 10k usuarios con google

#este tipo de login espero que tambien funcione contigo ivan
app.secret_key = '1234'  

app.register_blueprint(facturas_bp, url_prefix='/facturas')
app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
app.register_blueprint(gastos_bp, url_prefix='/gastos')

# Configura OAuth para la verificacion de google
#oauth = OAuth(app)
#google = oauth.register(
#    name='google',
#    client_id='818050231644-68l5cd6c0hvg9ihh947guetml63381nr.apps.googleusercontent.com',
#    client_secret='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',
#    authorize_url='https://accounts.google.com/o/oauth2/auth',
#    authorize_params=None,
#    access_token_url='https://accounts.google.com/o/oauth2/token',
#    access_token_params=None,
#    refresh_token_url=None,
#    redirect_uri='http://127.0.0.1:5000/auth/callback',
#    client_kwargs={'scope': 'openid profile email'}
#)#
#
#

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

#Ruta para ISR

@app.route('/ISR')
def ISR():
    return render_template('ISR.html')

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

@app.route('/loginlocal', methods=['POST','GET'])
def loginlocal():
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

# Ruta para manejar el login con Google (NO FUNCIONAL)
    
#@app.route('/login' , methods=['GET', 'POST'])
#def login():
#    redirect_uri = url_for('authorized', _external=True)
#    return google.authorize_redirect(redirect_uri)#

#@app.route('/auth/callback')
#def authorized():
#    print("Iniciando la autorización...")
#    token = google.authorize_access_token()
#    print("Token obtenido:", token)
#    if not token:
#        return "Error: No se pudo obtener el token de acceso."
#    user_info = google.parse_id_token(token)
#    print("Información del usuario:", user_info)
#    if not user_info:
#        return "Error: No se pudo obtener la información del usuario."
#    session['user_info'] = user_info
#    return 'Logged in as: ' + user_info['email']#
#

#@app.route('/logout')
#def logout():
#    session.pop('user_info', None)
#    return redirect('/')#

if __name__ == '__main__':
   app.run(debug=True)