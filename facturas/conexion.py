import mysql.connector

import mysql.connector
conexion = mysql.connector.connect(user= 'root', password= '',
                                    host= 'localhost',
                                    database= 'univai',
                                    port='3306')
print(conexion)
