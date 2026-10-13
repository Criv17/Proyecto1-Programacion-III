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
#orden 
 
lista_cursos = [
    (1, "1111111111111111", "Hoja de Calculo G2", "2026-08-17", "2026-10-01", "Activo", "Audie R. Ruiz Ortega", "69", "2.0", "AGOSTO"),
    (2, "2222222222222222222222222", "Hoja de Calculo G1", "2026-08-17", "2026-10-01", "Activo", "Audie R. Ruiz Ortega", "69", "2.0", "AGOSTO"),
]
 
siguiente_id_curso = 3
 
 #funciones para reemplazar despues con sql#
def db_listar_cursos():
    # El mas reciente primero
    return sorted(lista_cursos, key=lambda fila: fila[0], reverse=True)
 
 
def db_insertar_curso(datos):
    global siguiente_id_curso
    lista_cursos.append((siguiente_id_curso, *datos))
    siguiente_id_curso += 1
 
 
def db_actualizar_curso(id_curso, datos):
    for i, fila in enumerate(lista_cursos):
        if str(fila[0]) == str(id_curso):
            lista_cursos[i] = (fila[0], *datos)
 
 
def db_eliminar_curso(id_curso):
    lista_cursos[:] = [
        fila for fila in lista_cursos
        if str(fila[0]) != str(id_curso)
    ]
 
 
#Funciones#
 
def cargar_cursos():
    for item in tabla_cursos.get_children():
        tabla_cursos.delete(item)
 
    datos = db_listar_cursos()
 
    for fila in datos:
        tabla_cursos.insert("", tk.END, values=fila)
 
    lbl_total_cursos.config(
        text=f"Total cursos: {len(datos)}"
    )
 
 
def limpiar_curso():
 
    txt_id_curso.config(state="normal")
    txt_id_curso.delete(0, tk.END)
    txt_id_curso.config(state="readonly")
 
    txt_referencia.delete(0, tk.END)
    txt_descripcion.delete(0, tk.END)
 
    txt_fecha_inicio.set_date(date.today())
    txt_fecha_final.set_date(date.today())
 
    cmb_estado.set("Activo")
 
    txt_docente.delete(0, tk.END)
    txt_horas_cap.delete(0, tk.END)
    txt_horas_ase.delete(0, tk.END)
    txt_mes.delete(0, tk.END)
 
 
def validar_curso():
    # Devuelve true si los datos estan bien false si hay algun error
 
    if not txt_referencia.get():
        messagebox.showerror(
            "Error",
            "Digite la referencia"
        )
        return False
 
    # las horas son opcionales, pero si se escriben deben ser numeros
    for campo, nombre in (
        (txt_horas_cap, "Horas de Capacitacion"),
        (txt_horas_ase, "Horas de Asesoria")
    ):
        if campo.get():
            try:
                float(campo.get())
            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"{nombre} debe ser un numero"
                )
                return False
 
    if txt_fecha_final.get() < txt_fecha_inicio.get():
        messagebox.showerror(
            "Error",
            "La fecha final no puede ser menor a la fecha de inicio"
        )
        return False
 
    return True
 
 
def leer_form_curso():
    return (
        txt_referencia.get(),
        txt_descripcion.get(),
        txt_fecha_inicio.get(),
        txt_fecha_final.get(),
        cmb_estado.get(),
        txt_docente.get(),
        txt_horas_cap.get(),
        txt_horas_ase.get(),
        txt_mes.get()
    )
 
 
def agregar_curso():
    if not validar_curso():
        return
 
    db_insertar_curso(leer_form_curso())
 
    cargar_cursos()
    limpiar_curso()
 
    messagebox.showinfo(
        "Exito",
        "Hecho correctamente"
    )
 
 
def actualizar_curso():
 
    if txt_id_curso.get() == "":
        return
 
    if not validar_curso():
        return
 
    db_actualizar_curso(
        txt_id_curso.get(),
        leer_form_curso()
    )
 
    cargar_cursos()
 
    messagebox.showinfo(
        "Actualizado",
        "Registro actualizado"
    )
 
 
def eliminar_curso():
 
    if txt_id_curso.get() == "":
        return
 
    respuesta = messagebox.askyesno(
        "Eliminar",
        "Desea eliminar el curso?"
    )
 
    if respuesta:
 
        db_eliminar_curso(txt_id_curso.get())
 
        cargar_cursos()
        limpiar_curso()
 
 
def seleccionar_curso(event):
    fila = tabla_cursos.focus()
 
    if not fila:
        return
 
    datos = tabla_cursos.item(
        fila,
        "values"
    )
 
    txt_id_curso.config(state="normal")
    txt_id_curso.delete(0, tk.END)
    txt_id_curso.insert(0, datos[0])
    txt_id_curso.config(state="readonly")
 
    txt_referencia.delete(0, tk.END)
    txt_descripcion.delete(0, tk.END)
    txt_docente.delete(0, tk.END)
    txt_horas_cap.delete(0, tk.END)
    txt_horas_ase.delete(0, tk.END)
    txt_mes.delete(0, tk.END)
 
    txt_referencia.insert(0, datos[1])
    txt_descripcion.insert(0, datos[2])
    txt_fecha_inicio.set_date(datos[3])
    txt_fecha_final.set_date(datos[4])
    cmb_estado.set(datos[5])
    txt_docente.insert(0, datos[6])
    txt_horas_cap.insert(0, datos[7])
    txt_horas_ase.insert(0, datos[8])
    txt_mes.insert(0, datos[9])
 
 

# interfaz #
# llama a ventana principal y recibe el Frame de la pestaña #

 
def crear_tab(parent):
 
  #globales para usar arriba
    global txt_id_curso, txt_referencia, txt_descripcion
    global txt_fecha_inicio, txt_fecha_final, cmb_estado
    global txt_docente, txt_horas_cap, txt_horas_ase, txt_mes
    global tabla_cursos, lbl_total_cursos
 
    # frame
 
    frame_datos_curso = tk.LabelFrame(
 
        parent,
        text="Datos del Curso",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=10
 
    )
 
    frame_datos_curso.pack(
        fill="x",
        padx=15,
        pady=10
    )
 
    #grid de cursos
 
    # ID (no se muestra, solo guarda el ID del curso seleccionado)
    txt_id_curso = tk.Entry(frame_datos_curso, state="readonly")
 
    # referencia
    tk.Label(frame_datos_curso, text="Referencia").grid(row=0, column=0, pady=5, sticky="w")
    txt_referencia = tk.Entry(frame_datos_curso, width=40)
    txt_referencia.grid(row=0, column=1, sticky="w", padx=(10, 40))
 
    # descripcion
    tk.Label(frame_datos_curso, text="Descripcion").grid(row=1, column=0, pady=5, sticky="w")
    txt_descripcion = tk.Entry(frame_datos_curso, width=40)
    txt_descripcion.grid(row=1, column=1, sticky="w", padx=(10, 40))
 
    #fecha de inicio
    tk.Label(frame_datos_curso, text="Fecha Inicio").grid(row=2, column=0, pady=5, sticky="w")
    txt_fecha_inicio = DateEntry(
        frame_datos_curso,
        width=17,
        date_pattern="yyyy-mm-dd"
    )
    txt_fecha_inicio.grid(row=2, column=1, sticky="w", padx=(10, 40))
 
    #fecha final
    tk.Label(frame_datos_curso, text="Fecha Final").grid(row=3, column=0, pady=5, sticky="w")
    txt_fecha_final = DateEntry(
        frame_datos_curso,
        width=17,
        date_pattern="yyyy-mm-dd"
    )
    txt_fecha_final.grid(row=3, column=1, sticky="w", padx=(10, 40))
 
    # estado
    tk.Label(frame_datos_curso, text="Estado").grid(row=4, column=0, pady=5, sticky="w")
    cmb_estado = ttk.Combobox(
        frame_datos_curso,
        width=15,
        state="readonly",
        values=[
            "Activo",
            "Inactivo",
            "Finalizado"
        ]
    )
    cmb_estado.grid(row=4, column=1, sticky="w", padx=(10, 40))
    cmb_estado.set("Activo")
 
    # profesor
    tk.Label(frame_datos_curso, text="Docente").grid(row=0, column=2, pady=5, sticky="w")
    txt_docente = tk.Entry(frame_datos_curso, width=40)
    txt_docente.grid(row=0, column=3, sticky="w", padx=10)
 
    # Horas de capacitacion
    tk.Label(frame_datos_curso, text="Horas de Capacitacion").grid(row=1, column=2, pady=5, sticky="w")
    txt_horas_cap = tk.Entry(frame_datos_curso, width=15)
    txt_horas_cap.grid(row=1, column=3, sticky="w", padx=10)
 
    #Horas de asesoria
    tk.Label(frame_datos_curso, text="Horas de Asesoria").grid(row=2, column=2, pady=5, sticky="w")
    txt_horas_ase = tk.Entry(frame_datos_curso, width=15)
    txt_horas_ase.grid(row=2, column=3, sticky="w", padx=10)
 
    #Mes
    tk.Label(frame_datos_curso, text="Mes").grid(row=3, column=2, pady=5, sticky="w")
    txt_mes = tk.Entry(frame_datos_curso, width=15)
    txt_mes.grid(row=3, column=3, sticky="w", padx=10)
 
    # botones
 
    frame_botones_curso = tk.Frame(frame_datos_curso)
    frame_botones_curso.grid(row=5, column=0, columnspan=4, pady=10)
 
    tk.Button(
        frame_botones_curso,
        text="Guardar",
        width=15,
        bg="#27AE60",
        fg="white",
        command=agregar_curso
    ).grid(row=0, column=0, padx=5)
 
    tk.Button(
        frame_botones_curso,
        text="Actualizar",
        width=15,
        bg="#2980B9",
        fg="white",
        command=actualizar_curso
    ).grid(row=0, column=1, padx=5)
 
    tk.Button(
        frame_botones_curso,
        text="Eliminar",
        width=15,
        bg="#C0392B",
        fg="white",
        command=eliminar_curso
    ).grid(row=0, column=2, padx=5)
 
    tk.Button(
        frame_botones_curso,
        text="Limpiar",
        width=15,
        command=limpiar_curso
    ).grid(row=0, column=3, padx=5)
 
    # Tabla/grid
 
    frame_lista_curso = tk.LabelFrame(
 
        parent,
        text="Listado de Cursos",
        font=("Segoe UI", 10, "bold")
    )
 
    frame_lista_curso.pack(
 
        fill="both",
        expand=True,
        padx=15,
        pady=5
    )
 
    scroll_y_curso = ttk.Scrollbar(frame_lista_curso, orient="vertical")
    scroll_x_curso = ttk.Scrollbar(frame_lista_curso, orient="horizontal")
 
    columnas_curso = (
        "ID",
        "REFERENCIA",
        "DESCRIPCION",
        "INICIO",
        "FINAL",
        "ESTADO",
        "DOCENTE",
        "HORAS CAP.",
        "HORAS ASES.",
        "MES"
    )
 
    # grid
    tabla_cursos = ttk.Treeview(
 
        frame_lista_curso,
        columns=columnas_curso,
        show="headings",
        height=5,
        yscrollcommand=scroll_y_curso.set,
        xscrollcommand=scroll_x_curso.set
 
    )
 
    scroll_y_curso.config(command=tabla_cursos.yview)
    scroll_x_curso.config(command=tabla_cursos.xview)
 
    for col in columnas_curso:
        tabla_cursos.heading(col, text=col)
 
    tabla_cursos.column("ID", width=40, anchor="center")
    tabla_cursos.column("REFERENCIA", width=260)
    tabla_cursos.column("DESCRIPCION", width=150)
    tabla_cursos.column("INICIO", width=90)
    tabla_cursos.column("FINAL", width=90)
    tabla_cursos.column("ESTADO", width=80)
    tabla_cursos.column("DOCENTE", width=160)
    tabla_cursos.column("HORAS CAP.", width=80, anchor="center")
    tabla_cursos.column("HORAS ASES.", width=80, anchor="center")
    tabla_cursos.column("MES", width=90)
 
    #evita que las columnas se encojan
    for col in columnas_curso:
        tabla_cursos.column(col, stretch=False)
 
    tabla_cursos.grid(row=0, column=0, sticky="nsew")
    scroll_y_curso.grid(row=0, column=1, sticky="ns")
    scroll_x_curso.grid(row=1, column=0, sticky="ew")
 
    frame_lista_curso.rowconfigure(0, weight=1)
    frame_lista_curso.columnconfigure(0, weight=1)
 
    tabla_cursos.bind(
        "<<TreeviewSelect>>",
        seleccionar_curso
    )
 
    #Pie de pagina
 
    lbl_total_cursos = tk.Label(
 
        parent,
        text="Total de cursos: 0",
        font=("Segoe UI", 10, "bold")
    )
 
    lbl_total_cursos.pack(pady=5)
 
    cargar_cursos()