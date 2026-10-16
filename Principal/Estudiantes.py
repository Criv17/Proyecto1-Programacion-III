# Inicio de proyecto 1 de Programacion III
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry
#from Estudiantes import Estudiantes
from PYTHON.Estudiantes import Estudiantes


# Objeto que conecta la interfaz con las operaciones de estudiantes
gestor_estudiantes = Estudiantes()


# Funciones principales de la interfaz

def cargar_datos():
    # Borra las filas que ya aparecen en la tabla
    for item in tabla.get_children():
        tabla.delete(item)

    try:
        # Obtiene los estudiantes desde SQL Server
        datos = gestor_estudiantes.listar()

        # Muestra cada estudiante en la tabla
        for fila in datos:
            tabla.insert("", tk.END, values=tuple(fila))

        lbl_total.config(text=f"Total estudiantes: {len(datos)}")

    except Exception as error:
        messagebox.showerror("Error de conexion", str(error))


def limpiar():
    txt_id.config(state="normal")
    txt_id.delete(0, tk.END)
    txt_id.config(state="readonly")

    txt_cedula.config(state="normal")
    txt_cedula.delete(0, tk.END)

    txt_nombre.delete(0, tk.END)
    txt_apellidos.delete(0, tk.END)

    txt_nacimiento.set_date(date.today())

    txt_correo.delete(0, tk.END)
    txt_celular.delete(0, tk.END)
    txt_padre.delete(0, tk.END)
    txt_cel_padre.delete(0, tk.END)


def obtener_datos():
    # Devuelve los datos en el mismo orden que los recibe Estudiantes.py
    return (
        txt_cedula.get().strip(),
        txt_nombre.get().strip(),
        txt_apellidos.get().strip(),
        txt_nacimiento.get(),
        txt_correo.get().strip(),
        txt_celular.get().strip(),
        txt_padre.get().strip(),
        txt_cel_padre.get().strip()
    )


def agregar():
    datos = obtener_datos()

    try:
        # El método registrar valida los datos y los guarda en SQL Server
        gestor_estudiantes.registrar(*datos)

        cargar_datos()
        limpiar()
        messagebox.showinfo("Exito", "Estudiante guardado.")

    except Exception as error:
        messagebox.showerror("No se pudo registrar", str(error))


def actualizar():
    if txt_id.get() == "":
        messagebox.showwarning(
            "Seleccionar estudiante",
            "Seleccione un estudiante de la tabla antes de actualizar."
        )
        return

    datos = obtener_datos()

    try:
        # La cédula se conserva como identificador, por eso queda bloqueada
        # al seleccionar un estudiante. Los demás datos sí se pueden cambiar.
        gestor_estudiantes.modificar(*datos)

        cargar_datos()
        limpiar()
        messagebox.showinfo("Actualizado", "Registro actualizado.")

    except Exception as error:
        messagebox.showerror("No se pudo actualizar", str(error))


def eliminar():
    if txt_id.get() == "":
        messagebox.showwarning(
            "Seleccionar estudiante",
            "Seleccione un estudiante de la tabla antes de eliminar."
        )
        return

    respuesta = messagebox.askyesno(
        "Eliminar",
        "Desea eliminar el estudiante?"
    )

    if respuesta:
        try:
            # El método eliminar recibe la cédula del estudiante seleccionado
            gestor_estudiantes.eliminar(txt_cedula.get())

            cargar_datos()
            limpiar()
            messagebox.showinfo("Eliminado", "Estudiante eliminado.")

        except Exception as error:
            messagebox.showerror("No se pudo eliminar", str(error))


def seleccionar(event):
    fila = tabla.focus()

    if not fila:
        return

    datos = tabla.item(fila, "values")

    txt_id.config(state="normal")
    txt_id.delete(0, tk.END)
    txt_id.insert(0, datos[0])
    txt_id.config(state="readonly")

    # La cédula se usa para localizar el registro en modificar/eliminar.
    # Se bloquea durante la edición para evitar que deje de coincidir.
    txt_cedula.config(state="normal")
    txt_cedula.delete(0, tk.END)
    txt_cedula.insert(0, datos[1])
    txt_cedula.config(state="readonly")

    txt_nombre.delete(0, tk.END)
    txt_apellidos.delete(0, tk.END)
    txt_correo.delete(0, tk.END)
    txt_celular.delete(0, tk.END)
    txt_padre.delete(0, tk.END)
    txt_cel_padre.delete(0, tk.END)

    txt_nombre.insert(0, datos[2])
    txt_apellidos.insert(0, datos[3])
    txt_nacimiento.set_date(datos[4])
    txt_correo.insert(0, datos[5] if datos[5] is not None else "")
    txt_celular.insert(0, datos[6] if datos[6] is not None else "")
    txt_padre.insert(0, datos[7] if datos[7] is not None else "")
    txt_cel_padre.insert(0, datos[8] if datos[8] is not None else "")


# Interfaz: la llama Ventana_principal.py y recibe el Frame de la pestaña

def crear_tab(parent):
    # Globales para usar los controles en las funciones de arriba
    global txt_id, txt_cedula, txt_nombre, txt_apellidos, txt_nacimiento
    global txt_correo, txt_celular, txt_padre, txt_cel_padre
    global tabla, lbl_total

    # Frame de datos
    frame_datos = tk.LabelFrame(
        parent,
        text="Datos del Estudiante",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=10
    )
    frame_datos.pack(fill="x", padx=15, pady=10)

    # ID
    tk.Label(frame_datos, text="ID").grid(row=0, column=0, pady=5, sticky="w")
    txt_id = tk.Entry(frame_datos, width=10, state="readonly")
    txt_id.grid(row=0, column=1, sticky="w")

    # Cedula
    tk.Label(frame_datos, text="Cedula").grid(row=1, column=0, pady=5, sticky="w")
    txt_cedula = tk.Entry(frame_datos, width=30)
    txt_cedula.grid(row=1, column=1)

    # Nombre
    tk.Label(frame_datos, text="Nombre").grid(row=2, column=0, pady=5, sticky="w")
    txt_nombre = tk.Entry(frame_datos, width=30)
    txt_nombre.grid(row=2, column=1)

    # Apellidos
    tk.Label(frame_datos, text="Apellidos").grid(row=3, column=0, pady=5, sticky="w")
    txt_apellidos = tk.Entry(frame_datos, width=30)
    txt_apellidos.grid(row=3, column=1)

    # Fecha de nacimiento
    tk.Label(frame_datos, text="Fecha Nacimiento").grid(row=4, column=0, pady=5, sticky="w")
    txt_nacimiento = DateEntry(
        frame_datos,
        width=27,
        date_pattern="yyyy-mm-dd"
    )
    txt_nacimiento.grid(row=4, column=1)

    # Correo
    tk.Label(frame_datos, text="Correo electronico").grid(row=5, column=0, pady=5, sticky="w")
    txt_correo = tk.Entry(frame_datos, width=30)
    txt_correo.grid(row=5, column=1)

    # Celular del estudiante
    tk.Label(frame_datos, text="Celular del estudiante").grid(row=6, column=0, pady=5, sticky="w")
    txt_celular = tk.Entry(frame_datos, width=30)
    txt_celular.grid(row=6, column=1)

    # Encargado
    tk.Label(frame_datos, text="Nombre del padre/encargado").grid(row=1, column=2, padx=20, sticky="w")
    txt_padre = tk.Entry(frame_datos, width=30)
    txt_padre.grid(row=1, column=3)

    # Celular del encargado
    tk.Label(frame_datos, text="Celular del padre/encargado").grid(row=2, column=2, padx=20, sticky="w")
    txt_cel_padre = tk.Entry(frame_datos, width=30)
    txt_cel_padre.grid(row=2, column=3)

    # Botones
    frame_botones = tk.Frame(frame_datos)
    frame_botones.grid(row=7, column=0, columnspan=4, pady=10)

    tk.Button(
        frame_botones,
        text="Guardar",
        width=15,
        bg="#27AE60",
        fg="white",
        command=agregar
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        frame_botones,
        text="Actualizar",
        width=15,
        bg="#2980B9",
        fg="white",
        command=actualizar
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        frame_botones,
        text="Eliminar",
        width=15,
        bg="#C0392B",
        fg="white",
        command=eliminar
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        frame_botones,
        text="Limpiar",
        width=15,
        command=limpiar
    ).grid(row=0, column=3, padx=5)

    # Tabla/listado
    frame_lista = tk.LabelFrame(
        parent,
        text="Listado de Estudiantes",
        font=("Segoe UI", 10, "bold")
    )
    frame_lista.pack(fill="both", expand=True, padx=15, pady=5)

    scroll_y = ttk.Scrollbar(frame_lista, orient="vertical")
    scroll_x = ttk.Scrollbar(frame_lista, orient="horizontal")

    columnas = (
        "ID",
        "CEDULA",
        "NOMBRE",
        "APELLIDOS",
        "NACIMIENTO",
        "CORREO",
        "CELULAR",
        "PADRE/ENCARGADO",
        "CELULAR ENCARGADO"
    )

    tabla = ttk.Treeview(
        frame_lista,
        columns=columnas,
        show="headings",
        height=5,
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    for col in columnas:
        tabla.heading(col, text=col)

    tabla.column("ID", width=40, anchor="center")
    tabla.column("CEDULA", width=100)
    tabla.column("NOMBRE", width=130)
    tabla.column("APELLIDOS", width=150)
    tabla.column("NACIMIENTO", width=90)
    tabla.column("CORREO", width=160)
    tabla.column("CELULAR", width=90)
    tabla.column("PADRE/ENCARGADO", width=130)
    tabla.column("CELULAR ENCARGADO", width=120)

    # Evita que las columnas se encojan; así aparece el scroll horizontal
    for col in columnas:
        tabla.column(col, stretch=False)

    tabla.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    frame_lista.rowconfigure(0, weight=1)
    frame_lista.columnconfigure(0, weight=1)

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # Pie de página
    lbl_total = tk.Label(
        parent,
        text="Total de estudiantes: 0",
        font=("Segoe UI", 10, "bold")
    )
    lbl_total.pack(pady=5)

    cargar_datos()
