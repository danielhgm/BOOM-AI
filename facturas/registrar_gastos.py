from flask import Flask, render_template, request, jsonify, Blueprint
import mysql.connector
from mysql.connector import Error

gastos_bp = Blueprint('gastos', __name__, template_folder='templates')

# Configuración de la conexión a la base de datos
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



# Ruta para mostrar el formulario de registro de gastos
@gastos_bp.route('/registrar_gastos', methods=['GET'])
def mostrar_formulario():
    return render_template('registrar_gastos.html')

# Ruta para registrar un nuevo gasto
@gastos_bp.route('/registrar_gastos', methods=['POST'])
def registrar_gasto():
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser 'application/json'"}), 400
    
    data = request.get_json()
    
    descripcion = data.get('descripcion')
    monto = data.get('monto')
    fecha = data.get('fecha')

    connection = db_connect()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO gastos (descripcion, monto, fecha) VALUES ( %s, %s,%s)"
        cursor.execute(sql, (descripcion, monto, fecha))
        connection.commit()
        return jsonify({"message": "Gasto registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
