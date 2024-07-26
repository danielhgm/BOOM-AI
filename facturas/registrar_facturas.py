from flask import Flask, jsonify, request
import pymysql.cursors


###
# Parece que intentaste acceder a la ruta /rf
# con una solicitud GET, pero esa ruta está configurada
# para aceptar solo solicitudes POST.



app = Flask(__name__)

def db_connect():
    return pymysql.connect(
        host='localhost',        # Dirección del servidor de la base de datos (local)
        port=3306,               # Puerto en el que está escuchando MySQL (3306 por defecto)
        user='root',             # Nombre de usuario de la base de datos
        password='1234',         # Contraseña del usuario de la base de datos
        db='boomai',             # Nombre de la base de datos a la que te estás conectando
        charset='utf8mb4',       # Conjunto de caracteres a utilizar
        cursorclass=pymysql.cursors.DictCursor  # Tipo de cursor para retornar resultados como diccionarios
    )

##@app.route('/')
# def index():
# return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
    return "Servidor Flask en funcionamiento"

@app.route('/registrar_facturas', methods=['POST'])
def registrar_facturas():
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser 'application/json'"}), 400
    data = request.get_json()
    
    producto_id = data.get('producto_id')
    proveedor_id = data.get('proveedor_id')
    cantidad = data.get('cantidad')
    fecha = data.get('fecha')

    connection = db_connect()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO facturas (producto_id, proveedor_id, cantidad, fecha) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (producto_id, proveedor_id, cantidad, fecha))
            connection.commit()
        return jsonify({"message": "Registro de factura exitoso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':    
    app.run(debug=True)