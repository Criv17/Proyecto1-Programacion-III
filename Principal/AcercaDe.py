#Ventana "Acerca de" del sistema
import tkinter as tk

def mostrar_acercade(root):
    # ventana con la informacion del sistema
    ventana = tk.Toplevel(root)
    ventana.title("Acerca de")
    ventana.resizable(False, False)
    ventana.transient(root)
 
    frame_info = tk.LabelFrame(
        ventana,
        text="Información del sistema",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=10
    )
    frame_info.pack(fill="both", expand=True, padx=15, pady=10)
 
    #dDATAOS APARA MSOTRAR EN LA VENTANA DE ACERCA DE
    datos = (
        ("Sistema:", "Sistema de Control Académico y Asistencias"),
        ("Versión:", "1.0"),
        ("Curso:", "Programación III"),
        ("Docente:", "Audie Ruiz"),
        ("Autores:", "Ismael Valverde\nIsabel Gonzalez"),
        ("Fecha:", "17 Octubre 2026"),
        ("Descripción:",
         "Programa para llevar el control de estudiantes, cursos, "
         "matrículas y asistencias de un centro academico "
         "En cada pestaña se puede registrar, modificar, eliminar y "
         "consultar información, que queda guardada en una base de datos. "
        )
    )
 
    for fila, (etiqueta, valor) in enumerate(datos):
        tk.Label(
            frame_info,
            text=etiqueta,
            font=("Segoe UI", 10, "bold")
        ).grid(row=fila, column=0, sticky="nw", pady=4)
 
        tk.Label(
            frame_info,
            text=valor,
            justify="left",
            wraplength=320
        ).grid(row=fila, column=1, sticky="w", padx=10, pady=4)
 
    # Boton CERRAR el acerca de
    tk.Button(
        ventana,
        text="Cerrar",
        width=15,
        bg="#7C0376",
        fg="white",
        command=ventana.destroy
    ).pack(pady=(0, 15))
 
    # se ajusta al contenido y se centra sobre la ventana principal
    ventana.update_idletasks()
    ancho_v = ventana.winfo_reqwidth()
    alto_v = ventana.winfo_reqheight()
    x_v = root.winfo_x() + (root.winfo_width() // 2) - (ancho_v // 2)
    y_v = root.winfo_y() + (root.winfo_height() // 2) - (alto_v // 2)
    ventana.geometry(f"{ancho_v}x{alto_v}+{x_v}+{y_v}")
 
    ventana.grab_set()  # bloquea la ventana principal hasta cerrar esta