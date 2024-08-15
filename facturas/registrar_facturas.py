from flask import Flask, request, jsonify, render_template, Blueprint
import mysql.connector
from mysql.connector import Error



app = Flask(__name__)


facturas_bp = Blueprint('facturas', __name__, template_folder='templates')

def db_connect():
    try:
        connection =mysql.connector.connect(
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

@facturas_bp.route('/menu_facturas', methods=['GET'])
def menu_facturas():
    return render_template('menu_facturas.html')


@facturas_bp.route('/registrar_facturas', methods=['GET'])
def mostrar_formulario():
    return render_template('registrar_facturas.html')

@facturas_bp.route('/registrar_facturas', methods=['POST'])
def registrar_facturas():
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser 'application/json'"}), 400
    
    data = request.get_json()
    
    producto_id = data.get('producto_id')
    proveedor_id = data.get('proveedor_id')
    cantidad = data.get('cantidad')
    fecha = data.get('fecha')

    connection = db_connect()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO productos (producto_id, proveedor_id, cantidad, fecha) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (producto_id, proveedor_id, cantidad, fecha))
        connection.commit()
        return jsonify({"message": "Registro de factura exitoso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)