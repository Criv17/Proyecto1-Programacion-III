
from ConexionSQL import ConexionSQL

conexion = ConexionSQL.conectar()

if conexion:
    print("Conexion exitosa a la bd")
    conexion.close()
else:
    print("No se pudo conectar a la bd")
    
    