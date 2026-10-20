import pyodbc
from tkinter import messagebox
 
 
def conectar():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=(localdb)\MSSQLLocalDB;"                 
        "DATABASE=ControlAcademico;"
        "Trusted_Connection=yes;"           
        "TrustServerCertificate=yes;",
        #timeout=5
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