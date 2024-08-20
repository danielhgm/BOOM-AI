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




# Nueva ruta para consultar todos los proveedores
@proveedores_bp.route('/consultar_proveedores', methods=['GET'])
def consultar_proveedores():
    connection = db_connect()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM proveedores")
        proveedores = cursor.fetchall()
        return render_template('consulta_proveedores.html', proveedores=proveedores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()