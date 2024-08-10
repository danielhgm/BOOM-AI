from flask import Blueprint, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

# Define el Blueprint para proveedores
proveedores_bp = Blueprint('proveedores', __name__, template_folder='templates')

# Función para conectar a la base de datos
def db_connect():
    try:
        connection = mysql.connector.connect(
            user='virtualbox1',
            password='Altima_2800',
            host='172.29.193.211',
            database='boomai',
            port='3306'
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Ruta para mostrar el formulario de registro de proveedores
@proveedores_bp.route('/registrar_proveedores', methods=['GET'])
def mostrar_formulario():
    return render_template('registrar_proveedores.html')

# Ruta para registrar un proveedor en la base de datos
@proveedores_bp.route('/registrar_proveedores', methods=['POST'])
def registrar_proveedor():
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser 'application/json'"}), 400
    
    data = request.get_json()
    
    proveedor_id = data.get('proveedor_id')
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    telefono = data.get('telefono')

    connection = db_connect()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO proveedores (proveedor_id, nombre, direccion, telefono) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (proveedor_id, nombre, direccion, telefono))
        connection.commit()
        return jsonify({"message": "Proveedor registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Nueva ruta para consultar todos los proveedores
@proveedores_bp.route('/consultar_proveedores', methods=['GET'])
def consultar_proveedores():
    connection = db_connect()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor(dictionary=True)  # dictionary=True devuelve los resultados como diccionarios
        sql = "SELECT * FROM proveedores"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()