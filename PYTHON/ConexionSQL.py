import pyodbc


def conectar():
    conexion = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=(localdb)\\MSSQLLocalDB;"
        "DATABASE=ControlAcademico;"
        "Trusted_Connection=yes;"
    )

    return conexion


# Prueba de conexión
try:
    conexion = conectar()
    print("Conexión exitosa a ControlAcademico")
    conexion.close()

except Exception as e:
    print("Error de conexión:")
    print(e)