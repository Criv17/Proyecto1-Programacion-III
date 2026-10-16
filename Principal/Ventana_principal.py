#Crear Ventana y pestanas
#para que sea por capas
 
import tkinter as tk
from tkinter import ttk
 
import Estudiantes
import Cursos
import Matricula
 
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
 
# pestanas
 
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)
 
tab_estudiantes = tk.Frame(notebook)
tab_cursos = tk.Frame(notebook)
tab_matriculas = tk.Frame(notebook)
tab_asistencias = tk.Frame(notebook)
 
notebook.add(tab_estudiantes, text="Estudiantes")
notebook.add(tab_cursos, text="Cursos")
notebook.add(tab_matriculas, text="Matriculas")
notebook.add(tab_asistencias, text="Asistencias")
 
# Cada archivo construye su propia pestaña
 
Estudiantes.crear_tab(tab_estudiantes)
Cursos.crear_tab(tab_cursos)
Matricula.crear_tab(tab_matriculas)


 
root.mainloop()