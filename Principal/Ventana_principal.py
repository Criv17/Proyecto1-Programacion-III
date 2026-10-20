#Crear Ventana y pestanas
#para que sea por capas
 
import tkinter as tk
from tkinter import ttk, messagebox
 
import Estudiantes
import Cursos
import Matricula
import AcercaDe
 
# crear Ventana Principal
 
root = tk.Tk()
root.title("Sistema de Gestion Estudiantil")
root.configure(bg="#F4F6F7")
 
#centrar la Ventana
 
ancho = 1000
alto = 700
 
x = (root.winfo_screenwidth() // 2) - (ancho // 2)
y = (root.winfo_screenheight() // 2) - (alto // 2)
 
root.geometry(f"{ancho}x{alto}+{x}+{y}")
 
 
# opciones del sistema (Acerca de esta en Acerca.py)
 
def salir():
    # pide confirmacion y cierra el programa
    if messagebox.askyesno("Salir", "Desea cerrar el sistema?"):
        root.destroy()
 
 
def crear_tab_sistema(parent):
    # pestaña con las opciones del sistema (Acerca de y Salir)
    frame_opciones = tk.LabelFrame(
        parent,
        text="Opciones del sistema",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=10
    )
    frame_opciones.pack(fill="x", padx=15, pady=10)
 
    # Acerca de
    tk.Button(
        frame_opciones,
        text="Acerca de",
        width=15,
        bg="#FF7B0F",
        fg="white",
        command=lambda: AcercaDe.mostrar_acercade(root)
    ).grid(row=0, column=0, padx=5, pady=8)
 
    tk.Label(
        frame_opciones,
        text="Muestra la información del sistema"
    ).grid(row=0, column=1, sticky="w", padx=10)
 
    # Salir
    tk.Button(
        frame_opciones,
        text="Salir",
        width=15,
        bg="#7C0376",
        fg="white",
        command=salir
    ).grid(row=1, column=0, padx=5, pady=8)
 
    tk.Label(
        frame_opciones,
        text="Cierra el programa"
    ).grid(row=1, column=1, sticky="w", padx=10)
 
 
# pestanas
 
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)
 
tab_estudiantes = tk.Frame(notebook)
tab_cursos = tk.Frame(notebook)
tab_matriculas = tk.Frame(notebook)
tab_asistencias = tk.Frame(notebook)
tab_sistema = tk.Frame(notebook)
 
notebook.add(tab_estudiantes, text="Estudiantes")
notebook.add(tab_cursos, text="Cursos")
notebook.add(tab_matriculas, text="Matriculas")
notebook.add(tab_asistencias, text="Asistencias")
notebook.add(tab_sistema, text="Sistema")
 
# Cada archivo construye su propia pestaña
 
Estudiantes.crear_tab(tab_estudiantes)
Cursos.crear_tab(tab_cursos)
Matricula.crear_tab(tab_matriculas)
crear_tab_sistema(tab_sistema)

root.mainloop()
#root.protocol("WM_DELETE_WINDOW", salir)