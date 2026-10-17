import os
import pyodbc
from tkinter import messagebox

SERVIDORES = (
    "localhost",
    "(localdb)\\MSSQLLocalDB",
    "localhost\\SQLEXPRESS",
)

BASE_DE_DATOS = "ControlAcademico"

# Aqui se guarda el servidor que funciono, para no volver a probar los otros
servidor_activo = None


def servidores_a_probar():
    # Si existe el archivo servidor_local.txt (junto a este archivo), se usa
    # solo el servidor que diga ahi. Ese archivo es de cada computadora y
    # no se sube a GitHub, asi cada quien usa su servidor sin editar este codigo.
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "servidor_local.txt")

    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as archivo:
            servidor = archivo.read().strip()

        if servidor:
            return (servidor,)

    return SERVIDORES


def abrir(servidor):
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={servidor};"
        f"DATABASE={BASE_DE_DATOS};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;",
        timeout=15
    )


def conectar():
    global servidor_activo

    # Si ya se sabe cual servidor funciona, se usa directamente
    if servidor_activo is not None:
        return abrir(servidor_activo)

    errores = []

    for servidor in servidores_a_probar():
        try:
            conexion = abrir(servidor)
            servidor_activo = servidor
            return conexion
        except pyodbc.Error as error:
            errores.append(f"{servidor}: {str(error)[:150]}")

    raise pyodbc.Error(
        "No se pudo abrir la conexion a SQL Server. Servidores probados:\n"
        + "\n".join(errores)
    )


def consultar(sql, parametros=()):
    # Para select  ////// devuelve una lista de registros y lista vacia si hay error
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(sql, *parametros)
        filas = [tuple(fila) for fila in cursor.fetchall()]
        conn.close()
        return filas

    except pyodbc.Error as error:
        messagebox.showerror("Error de base de datos", str(error))
        return []


def ejecutar(sql, parametros=()):
    # Para insert update y delete /// devuelve verdadero si salio bien
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(sql, *parametros)
        conn.commit()
        conn.close()
        return True

    except pyodbc.Error as error:
        messagebox.showerror("Error de base de datos", str(error))
        return False