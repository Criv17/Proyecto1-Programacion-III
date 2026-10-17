import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
 
from Conexion import consultar, ejecutar
 
 
# Base de datos (SQL Server) #
 
def db_listar_matriculas():
    return consultar("""
        SELECT m.id, e.cedula, e.nombre, e.apellidos, c.referencia, c.descripcion, m.fecha_matricula, m.estado
        FROM Matriculas m
        INNER JOIN Estudiantes e ON m.estudiante_id = e.id
        INNER JOIN Cursos c ON m.curso_id = c.id
        ORDER BY m.id DESC
    """)
 
 
def db_listar_estudiantes():
    return consultar("""
        SELECT id, cedula, nombre, apellidos
        FROM Estudiantes
        ORDER BY nombre
    """)
 
 
def db_listar_cursos():
    return consultar("""
        SELECT id, referencia, descripcion
        FROM Cursos
        ORDER BY referencia
    """)
 
 
def db_obtener_matricula(id_matricula):
    filas = consultar("""
        SELECT id, estudiante_id, curso_id, fecha_matricula, estado
        FROM Matriculas
        WHERE id = ?
    """, (id_matricula,))
 
    if filas:
        return filas[0]
    return None
 
 
def db_existe_matricula(id_estudiante, id_curso):
    filas = consultar("""
        SELECT COUNT(*)
        FROM Matriculas
        WHERE estudiante_id = ? AND curso_id = ?
    """, (id_estudiante, id_curso))
 
    return bool(filas) and filas[0][0] > 0
 
 
def db_insertar_matricula(id_estudiante, id_curso, fecha, estado):
    return ejecutar("""
        INSERT INTO Matriculas (estudiante_id, curso_id, fecha_matricula, estado)
        VALUES (?,?,?,?)
    """, (id_estudiante, id_curso, fecha, estado))
 
 
def db_actualizar_estado(id_matricula, estado):
    return ejecutar("""
        UPDATE Matriculas
        SET estado = ?
        WHERE id = ?
    """, (estado, id_matricula))
 
 
def db_eliminar_matricula(id_matricula):
    return ejecutar("""
        DELETE FROM Matriculas
        WHERE id = ?
    """, (id_matricula,))
 
 
#Funciones de la interfaz
 
# texto del combo - id se llenan en actualizar_combos()
mapa_estudiantes = {}
mapa_cursos = {}
 
 
def actualizar_combos():
    #vuelve a leer estudiantes y cursos para que aparezcan los nuevos
    global mapa_estudiantes, mapa_cursos
 
    mapa_estudiantes = {
        f"{fila[1]} - {fila[2]} {fila[3]}": fila[0]
        for fila in db_listar_estudiantes()
    }
 
    mapa_cursos = {
        f"{fila[1]} - {fila[2]}": fila[0]
        for fila in db_listar_cursos()
    }
 
    cmb_estudiante.config(values=list(mapa_estudiantes))
    cmb_curso.config(values=list(mapa_cursos))
 
 
def cargar_matriculas():
    for item in tabla_matriculas.get_children():
        tabla_matriculas.delete(item)
 
    datos = db_listar_matriculas()
 
    for fila in datos:
        tabla_matriculas.insert("", tk.END, values=fila)
 
    lbl_total_matriculas.config(
        text=f"Total matriculas: {len(datos)}"
    )
 
 
def limpiar_matricula():
 
    txt_id_matricula.config(state="normal")
    txt_id_matricula.delete(0, tk.END)
    txt_id_matricula.config(state="readonly")
 
    cmb_estudiante.set("")
    cmb_curso.set("")
    cmb_estado_mat.set("Activa")
 
 
def agregar_matricula():
    if not cmb_estudiante.get() or not cmb_curso.get():
        messagebox.showerror(
            "Error",
            "Seleccione el estudiante y el curso"
        )
        return
 
    id_estudiante = mapa_estudiantes.get(cmb_estudiante.get())
    id_curso = mapa_cursos.get(cmb_curso.get())
 
    if id_estudiante is None or id_curso is None:
        messagebox.showerror(
            "Error",
            "El estudiante o el curso ya no existen"
        )
        return
 
    if db_existe_matricula(id_estudiante, id_curso):
        messagebox.showerror(
            "Error",
            "El estudiante ya esta matriculado en ese curso"
        )
        return
 
    # si falla, db_insertar_matricula ya mostro el error
    if not db_insertar_matricula(
        id_estudiante,
        id_curso,
        date.today(),
        cmb_estado_mat.get()
    ):
        return
 
    cargar_matriculas()
    limpiar_matricula()
 
    messagebox.showinfo(
        "Exito",
        "Matricula realizada"
    )
 
 
def actualizar_estado_matricula():
 
    if txt_id_matricula.get() == "":
        return
 
    if not db_actualizar_estado(
        txt_id_matricula.get(),
        cmb_estado_mat.get()
    ):
        return
 
    cargar_matriculas()
 
    messagebox.showinfo(
        "Actualizado",
        "Estado actualizado"
    )
 
 
def eliminar_matricula():
 
    if txt_id_matricula.get() == "":
        return
 
    respuesta = messagebox.askyesno(
        "Eliminar",
        "Desea eliminar la matricula?"
    )
 
    if respuesta:
 
        if not db_eliminar_matricula(txt_id_matricula.get()):
            return
 
        cargar_matriculas()
        limpiar_matricula()
 
 
def seleccionar_matricula(event):
    fila = tabla_matriculas.focus()
 
    if not fila:
        return
 
    datos = tabla_matriculas.item(
        fila,
        "values"
    )
 
    txt_id_matricula.config(state="normal")
    txt_id_matricula.delete(0, tk.END)
    txt_id_matricula.insert(0, datos[0])
    txt_id_matricula.config(state="readonly")
 
    # la tabla no trae los ID del estudiante y el curso, se buscan aparte
    matricula = db_obtener_matricula(datos[0])
 
    if matricula is None:
        return
 
    for texto, id_estudiante in mapa_estudiantes.items():
        if id_estudiante == matricula[1]:
            cmb_estudiante.set(texto)
 
    for texto, id_curso in mapa_cursos.items():
        if id_curso == matricula[2]:
            cmb_curso.set(texto)
 
    cmb_estado_mat.set(matricula[4])
 
 
# interfaz #
# la llama Ventana_principal.py y recibe el Frame de la pestaña #
 
def crear_tab(parent):
 
    #globales para usar arriba
    global txt_id_matricula, cmb_estudiante, cmb_curso, cmb_estado_mat
    global tabla_matriculas, lbl_total_matriculas
 
    # Frame
 
    frame_datos_mat = tk.LabelFrame(
 
        parent,
        text="Gestion de Matriculas",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=10
 
    )
 
    frame_datos_mat.pack(
        fill="x",
        padx=15,
        pady=10
    )
 
    #Grid de matriculas#
 
    # ID (no se muestra, solo guarda el ID de la matricula seleccionada)
    txt_id_matricula = tk.Entry(frame_datos_mat, state="readonly")
 
    # Estudiante
    tk.Label(frame_datos_mat, text="Estudiante").grid(row=0, column=0, pady=5, sticky="w")
    cmb_estudiante = ttk.Combobox(
        frame_datos_mat,
        width=70,
        state="readonly"
    )
    cmb_estudiante.grid(row=0, column=1, sticky="w", padx=10)
 
    # Curso
    tk.Label(frame_datos_mat, text="Curso").grid(row=1, column=0, pady=5, sticky="w")
    cmb_curso = ttk.Combobox(
        frame_datos_mat,
        width=70,
        state="readonly"
    )
    cmb_curso.grid(row=1, column=1, sticky="w", padx=10)
 
    # Estado
    tk.Label(frame_datos_mat, text="Estado").grid(row=2, column=0, pady=5, sticky="w")
    cmb_estado_mat = ttk.Combobox(
        frame_datos_mat,
        width=20,
        state="readonly",
        values=[
            "Activa",
            "Inactiva",
            "Retirada"
        ]
    )
    cmb_estado_mat.grid(row=2, column=1, sticky="w", padx=10)
    cmb_estado_mat.set("Activa")
 
    # botones
 
    frame_botones_mat = tk.Frame(frame_datos_mat)
    frame_botones_mat.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")
 
    tk.Button(
        frame_botones_mat,
        text="Matricular",
        width=18,
        bg="#27AE60",
        fg="white",
        command=agregar_matricula
    ).grid(row=0, column=0, padx=5)
 
    tk.Button(
        frame_botones_mat,
        text="Actualizar Estado",
        width=18,
        bg="#2980B9",
        fg="white",
        command=actualizar_estado_matricula
    ).grid(row=0, column=1, padx=5)
 
    tk.Button(
        frame_botones_mat,
        text="Eliminar Matricula",
        width=18,
        bg="#C0392B",
        fg="white",
        command=eliminar_matricula
    ).grid(row=0, column=2, padx=5)
 
    tk.Button(
        frame_botones_mat,
        text="Limpiar",
        width=18,
        command=limpiar_matricula
    ).grid(row=0, column=3, padx=5)
 
    #Tabla/grid #
 
    frame_lista_mat = tk.LabelFrame(
 
        parent,
        text="Listado de Matriculas",
        font=("Segoe UI", 10, "bold")
    )
 
    frame_lista_mat.pack(
 
        fill="both",
        expand=True,
        padx=15,
        pady=5
    )
 
    scroll_y_mat = ttk.Scrollbar(frame_lista_mat, orient="vertical")
    scroll_x_mat = ttk.Scrollbar(frame_lista_mat, orient="horizontal")
 
    columnas_mat = (
        "ID",
        "CEDULA",
        "NOMBRE",
        "APELLIDOS",
        "CURSO",
        "DESCRIPCION",
        "FECHA",
        "ESTADO"
    )
 
    # grid #
    tabla_matriculas = ttk.Treeview(
 
        frame_lista_mat,
        columns=columnas_mat,
        show="headings",
        height=5,
        yscrollcommand=scroll_y_mat.set,
        xscrollcommand=scroll_x_mat.set
 
    )
    #scrollbar#
    scroll_y_mat.config(command=tabla_matriculas.yview)
    scroll_x_mat.config(command=tabla_matriculas.xview)
 
    for col in columnas_mat:
        tabla_matriculas.heading(col, text=col)
 
    tabla_matriculas.column("ID", width=40, anchor="center")
    tabla_matriculas.column("CEDULA", width=100)
    tabla_matriculas.column("NOMBRE", width=140)
    tabla_matriculas.column("APELLIDOS", width=150)
    tabla_matriculas.column("CURSO", width=260)
    tabla_matriculas.column("DESCRIPCION", width=150)
    tabla_matriculas.column("FECHA", width=90)
    tabla_matriculas.column("ESTADO", width=80)
 
    #evita que las columnas se encojan asi aparece el scroll horizontal
    for col in columnas_mat:
        tabla_matriculas.column(col, stretch=False)
 
    tabla_matriculas.grid(row=0, column=0, sticky="nsew")
    scroll_y_mat.grid(row=0, column=1, sticky="ns")
    scroll_x_mat.grid(row=1, column=0, sticky="ew")
 
    frame_lista_mat.rowconfigure(0, weight=1)
    frame_lista_mat.columnconfigure(0, weight=1)
 
    tabla_matriculas.bind(
        "<<TreeviewSelect>>",
        seleccionar_matricula
    )
 
    #pie de pagina
 
    lbl_total_matriculas = tk.Label(
 
        parent,
        text="Total de matriculas: 0",
        font=("Segoe UI", 10, "bold")
    )
 
    lbl_total_matriculas.pack(pady=5)
 
    actualizar_combos()
    cargar_matriculas()
 
    # cada vez que se abre esta pestaña se actualizan los combos
    parent.bind("<Map>", lambda evento: actualizar_combos())