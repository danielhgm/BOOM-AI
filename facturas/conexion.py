import mysql.connector

import mysql.connector
conexion = mysql.connector.connect(user= 'root', password= '1234',
                                    host= 'localhost',
                                    database= 'boomai',
                                    port='3307')
print(conexion)
