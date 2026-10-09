#Inicio de proyecto 1 de programacion III

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry


########## IMPORTANTE ##########
#pip install tkcalendar (en el cmd de la pc o en la terminal de visual studio code)
################################


# Datos / base de datos #


#datos temporales para probar 
#orden id, cedula,  Nombre,            Apellido,           f.nacimiento,  correo              telefono  encargado,          cedula encargado
lista_estudiantes = [
    (1, "305320901", "Ismael Fabian", "Valverde Artavia", "2001-05-07", "ismael@gmail.com", "88053038", "Natalia Artavia", "70151500"),
    (2, "120500106", "Daniel", "Flores", "2000-01-01", "daniel@gmail.com", "71232456", "Gerardo Flores", "71232400"),
    (10, "120190617", "Ana", "chinchilla", "2000-01-01", "", "", "", ""),
    (20, "120190617", "Mili", "quesada", "2000-01-01", "prueba", "", "", "prueba"),
]

siguiente_id = 21

#Metodos principales para manejar los estudiantes temporales (Hay que cambiarlos/quitarlos cuando usemos sql)#
def db_listar():       # select * from estudiantes
    return list(lista_estudiantes)


def db_insertar(datos):  #insert y identity#
    global siguiente_id
    lista_estudiantes.append((siguiente_id, *datos))
    siguiente_id += 1


def db_actualizar(id_estudiante, datos): #update xxxx where id = x#
    for i, fila in enumerate(lista_estudiantes):
        if str(fila[0]) == str(id_estudiante):
            lista_estudiantes[i] = (fila[0], *datos)


def db_eliminar(id_estudiante): #delete xxxxxx where id = x#
    lista_estudiantes[:] = [
        fila for fila in lista_estudiantes
        if str(fila[0]) != str(id_estudiante)
    ]


#Crear Ventana Principal

root = tk.Tk()
root.title("Sistema de Gestion Estudiantil")
root.configure(bg="#F4F6F7")

#Centrar la Ventana

ancho = 1000
alto = 550

x = (root.winfo_screenwidth() // 2) - (ancho // 2)
y = (root.winfo_screenheight() // 2) - (alto // 2)

root.geometry(f"{ancho}x{alto}+{x}+{y}")

#Funciones de la interfaz

def cargar_datos():
    for item in tabla.get_children():
        tabla.delete(item)

    datos = db_listar()

    for fila in datos:
        tabla.insert("", tk.END, values=fila)

    lbl_total.config(
        text=f"Total estudiantes: {len(datos)}"
    )


def limpiar():

    txt_id.config(state="normal")
    txt_id.delete(0, tk.END)
    txt_id.config(state="readonly")

    txt_cedula.delete(0, tk.END)
    txt_nombre.delete(0, tk.END)
    txt_apellidos.delete(0, tk.END)

    txt_nacimiento.set_date(date.today())

    txt_correo.delete(0, tk.END)
    txt_celular.delete(0, tk.END)
    txt_padre.delete(0, tk.END)
    txt_cel_padre.delete(0, tk.END)


def agregar():
    if not txt_cedula.get():
        messagebox.showerror(
            "Error",
            "Digite la cedula"
        )
        return

    db_insertar(
        (
            txt_cedula.get(),
            txt_nombre.get(),
            txt_apellidos.get(),
            txt_nacimiento.get(),
            txt_correo.get(),
            txt_celular.get(),
            txt_padre.get(),
            txt_cel_padre.get()
        )
    )

    cargar_datos()
    limpiar()

    messagebox.showinfo(
        "Exito",
        "Hecho correctamente"
    )


def actualizar():

    if txt_id.get() == "":
        return

    db_actualizar(
        txt_id.get(),
        (
            txt_cedula.get(),
            txt_nombre.get(),
            txt_apellidos.get(),
            txt_nacimiento.get(),
            txt_correo.get(),
            txt_celular.get(),
            txt_padre.get(),
            txt_cel_padre.get()
        )
    )

    cargar_datos()

    messagebox.showinfo(
        "Actualizado",
        "Registro actualizado"
    )


def eliminar():

    if txt_id.get() == "":
        return

    respuesta = messagebox.askyesno(
        "Eliminar",
        "Desea eliminar el estudiante?"
    )

    if respuesta:

        db_eliminar(txt_id.get())

        cargar_datos()
        limpiar()


def seleccionar(event):
    fila = tabla.focus()

    if not fila:
        return

    datos = tabla.item(
        fila,
        "values"
    )

    txt_id.config(state="normal")
    txt_id.delete(0, tk.END)
    txt_id.insert(0, datos[0])
    txt_id.config(state="readonly")

    txt_cedula.delete(0, tk.END)
    txt_nombre.delete(0, tk.END)
    txt_apellidos.delete(0, tk.END)
    
    txt_correo.delete(0, tk.END)
    txt_celular.delete(0, tk.END)
    txt_padre.delete(0, tk.END)
    txt_cel_padre.delete(0, tk.END)

    txt_cedula.insert(0, datos[1])
    txt_nombre.insert(0, datos[2])
    txt_apellidos.insert(0, datos[3])
    txt_nacimiento.set_date(datos[4])
    txt_correo.insert(0, datos[5])
    txt_celular.insert(0, datos[6])
    txt_padre.insert(0, datos[7])
    txt_cel_padre.insert(0, datos[8])


#Pestanas

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

tab_estudiantes = tk.Frame(notebook)
tab_cursos = tk.Frame(notebook)
tab_matriculas = tk.Frame(notebook)
tab_asistencias = tk.Frame(notebook)

notebook.add(tab_estudiantes, text="Estudiantes")
notebook.add(tab_cursos, text="Cursos")
notebook.add(tab_matriculas, text="Matriculas")
notebook.add(tab_asistencias, text="Asistencias no tenemos que hacerla en este avance")

# Frame

frame_datos = tk.LabelFrame(

    tab_estudiantes,
    text="Datos del Estudiante",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=10

)

frame_datos.pack(
    fill="x",
    padx=15,
    pady=10
)

#Grid de estudiantes#

# ID
tk.Label(frame_datos, text="ID").grid(row=0, column=0, pady=5, sticky="w")
txt_id = tk.Entry(frame_datos, width=10, state="readonly")
txt_id.grid(row=0, column=1, sticky="w")

# Cedula
tk.Label(frame_datos, text="Cedula").grid(row=1, column=0, pady=5, sticky="w")
txt_cedula = tk.Entry(frame_datos, width=30)
txt_cedula.grid(row=1, column=1)

#Nombre
tk.Label(frame_datos, text="Nombre").grid(row=2, column=0, pady=5, sticky="w")
txt_nombre = tk.Entry(frame_datos, width=30)
txt_nombre.grid(row=2, column=1)

#Apellidos
tk.Label(frame_datos, text="Apellidos").grid(row=3, column=0, pady=5, sticky="w")
txt_apellidos = tk.Entry(frame_datos, width=30)
txt_apellidos.grid(row=3, column=1)

# Fecha de nacimiento       tkcalendar
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

#Celular del estudiante
tk.Label(frame_datos, text="Celular del estudiante").grid(row=6, column=0, pady=5, sticky="w")
txt_celular = tk.Entry(frame_datos, width=30)
txt_celular.grid(row=6, column=1)

# encargado
tk.Label(frame_datos, text="Nombre del padre/encargado").grid(row=1, column=2, padx=20, sticky="w")
txt_padre = tk.Entry(frame_datos, width=30)
txt_padre.grid(row=1, column=3)

# Celular del encargado
tk.Label(frame_datos, text="Celular del padre/encargado").grid(row=2, column=2, padx=20, sticky="w")
txt_cel_padre = tk.Entry(frame_datos, width=30)
txt_cel_padre.grid(row=2, column=3)

# botones

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

#Tabla/grid #

frame_lista = tk.LabelFrame(

    tab_estudiantes,
    text="Listado de Estudiantes",
    font=("Segoe UI", 10, "bold")
)

frame_lista.pack(

    fill="both",
    expand=True,
    padx=15,
    pady=5
)

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

# grid #
tabla = ttk.Treeview(

    frame_lista,
    columns=columnas,
    show="headings",
    height=5,
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set

)
#scrollbar#
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

#evita que las columnas se encojan asi aparece el scroll horizontal
for col in columnas:
    tabla.column(col, stretch=False)

tabla.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

frame_lista.rowconfigure(0, weight=1)
frame_lista.columnconfigure(0, weight=1)

tabla.bind(
    "<<TreeviewSelect>>",
    seleccionar
)

# Pie de pagina

lbl_total = tk.Label(

    tab_estudiantes,
    text="Total de estudiantes: 0",
    font=("Segoe UI", 10, "bold")
)

lbl_total.pack(pady=5)

cargar_datos()
root.mainloop()
