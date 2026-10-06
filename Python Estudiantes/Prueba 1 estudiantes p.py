from Estudiantes import Estudiantes


# Crear un objeto de la clase Estudiantes
estudiantes = Estudiantes()

# Registrar un estudiante
estudiantes.registrar(
    "123456789",
    "Maria",
    "Gonzalez",
    "2003-05-20",
    "marilla@gmail.com",
    "89056734",
    "Juan Ramirez",
    "878904567"
)

# Obtener los estudiantes registrados
lista = estudiantes.listar()

# Mostrar los estudiantes
for estudiante in lista:
    print(estudiante)