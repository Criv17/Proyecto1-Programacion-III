#Inicio de proyecto 1 de programacion III

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry
import pyodbc
 
import Cursosbd
 
 
########## IMPORTANTE ##########
#pip install tkcalendar (en el cmd de la pc o en la terminal de visual studio code)
################################
 
 
modelo = Cursosbd.Cursos()
 
# filas que se muestran en la tabla: id -> fila
# (se usa al seleccionar, asi no se pierden ceros ni se ven valores None)
datos_cargados = {}
 
 
#Funciones de la interfaz
 
def cargar_cursos():
    for item in tabla_cursos.get_children():
        tabla_cursos.delete(item)
 
    datos_cargados.clear()
 
    try:
        filas = modelo.listar()
    except pyodbc.Error as error:
        messagebox.showerror("Error de base de datos", str(error))
        filas = []
 
    # El mas reciente primero
    for fila in reversed(filas):
        # la BD devuelve None en los campos vacios, en la tabla se ven vacios
        fila = tuple("" if valor is None else valor for valor in fila)
 
        # el estado viene como 1 o 0, en pantalla se ve como texto
        fila = fila[:5] + (modelo.estado_a_texto(fila[5]),) + fila[6:]
 
        datos_cargados[str(fila[0])] = fila
        tabla_cursos.insert("", tk.END, iid=str(fila[0]), values=fila)
 
    lbl_total_cursos.config(
        text=f"Total cursos: {len(filas)}"
    )
 
 
def leer_form_curso():
    # mismo orden que piden registrar() y modificar()
    return (
        txt_referencia.get().strip(),
        txt_descripcion.get().strip(),
        txt_fecha_inicio.get(),
        txt_fecha_final.get(),
        cmb_estado.get(),
        txt_docente.get().strip(),
        txt_horas_cap.get().strip(),
        txt_horas_ase.get().strip(),
        txt_mes.get().strip()
    )
 
 
def limpiar_curso():
 
    txt_id_curso.config(state="normal")
    txt_id_curso.delete(0, tk.END)
    txt_id_curso.config(state="readonly")
 
    txt_referencia.config(state="normal")
    txt_referencia.delete(0, tk.END)
    txt_descripcion.delete(0, tk.END)
 
    txt_fecha_inicio.set_date(date.today())
    txt_fecha_final.set_date(date.today())
 
    cmb_estado.set("Activo")
 
    txt_docente.delete(0, tk.END)
    txt_horas_cap.delete(0, tk.END)
    txt_horas_ase.delete(0, tk.END)
    txt_mes.delete(0, tk.END)
 
 
def agregar_curso():
 
    try:
        modelo.registrar(*leer_form_curso())
    except (ValueError, pyodbc.Error) as error:
        messagebox.showerror("Error", str(error))
        return
 
    cargar_cursos()
    limpiar_curso()
 
    messagebox.showinfo(
        "Exito",
        "Hecho correctamente"
    )
 
 
def actualizar_curso():
 
    if txt_id_curso.get() == "":
        return
 
    try:
        modelo.modificar(*leer_form_curso())
    except (ValueError, pyodbc.Error) as error:
        messagebox.showerror("Error", str(error))
        return
 
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
 
        try:
            modelo.eliminar(txt_referencia.get())
 
        except pyodbc.IntegrityError:
            # tiene matriculas o dias no laborados
            messagebox.showerror(
                "No se puede eliminar",
                "El curso tiene matriculas o dias no laborados registrados."
            )
            return
 
        except (ValueError, pyodbc.Error) as error:
            messagebox.showerror("Error", str(error))
            return
 
        cargar_cursos()
        limpiar_curso()
 
 
def seleccionar_curso(event):
    fila = datos_cargados.get(tabla_cursos.focus())
 
    if fila is None:
        return
 
    txt_id_curso.config(state="normal")
    txt_id_curso.delete(0, tk.END)
    txt_id_curso.insert(0, fila[0])
    txt_id_curso.config(state="readonly")
 
    # la referencia no se puede cambiar, sirve para localizar el curso
    txt_referencia.config(state="normal")
    txt_referencia.delete(0, tk.END)
    txt_referencia.insert(0, fila[1])
    txt_referencia.config(state="readonly")
 
    txt_descripcion.delete(0, tk.END)
    txt_docente.delete(0, tk.END)
    txt_horas_cap.delete(0, tk.END)
    txt_horas_ase.delete(0, tk.END)
    txt_mes.delete(0, tk.END)
 
    txt_descripcion.insert(0, fila[2])
    txt_fecha_inicio.set_date(fila[3])
    txt_fecha_final.set_date(fila[4])
    cmb_estado.set(fila[5])
    txt_docente.insert(0, fila[6])
    txt_horas_cap.insert(0, str(fila[7]))
    txt_horas_ase.insert(0, str(fila[8]))
    txt_mes.insert(0, fila[9])
 
 
# interfaz #
# la llama Ventana_principal.py y recibe el Frame de la pestaña #
 
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
 
    # estado (en la base de datos es 1 = Activo, 0 = Inactivo)
    tk.Label(frame_datos_curso, text="Estado").grid(row=4, column=0, pady=5, sticky="w")
    cmb_estado = ttk.Combobox(
        frame_datos_curso,
        width=15,
        state="readonly",
        values=[
            "Activo",
            "Inactivo"
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
 