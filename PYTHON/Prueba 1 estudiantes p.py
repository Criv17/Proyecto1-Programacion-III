from Estudiantes import Estudiantes


# Crear un objeto de la clase Estudiantes
estudiantes = Estudiantes()


# Cedula utilizada para las pruebas
cedula_prueba = "679934634699"


# Consultar si el estudiante ya existe
estudiante = estudiantes.consultar(cedula_prueba)


# Registrar solamente si no existe
if estudiante is None:

    print("PRUEBA 1: REGISTRAR")

    estudiantes.registrar(
        cedula_prueba,
        "Maria",
        "Gonzalez",
        "2003-05-20",
        "maria.prueba@gmail.com",
        "89056734",
        "Juan Ramirez",
        "87890456"
    )

else:
    print("El estudiante ya existe. Se continuara con las otras pruebas.")


# PRUEBA 2: LISTAR
print("\nPRUEBA 2: LISTAR")

lista = estudiantes.listar()

for estudiante in lista:
    print(estudiante)


# PRUEBA 3: CONSULTAR
print("\nPRUEBA 3: CONSULTAR")

estudiante = estudiantes.consultar(cedula_prueba)

if estudiante:
    print(estudiante)
else:
    print("No se encontro el estudiante.")


# PRUEBA 4: MODIFICAR
print("\nPRUEBA 4: MODIFICAR")

estudiantes.modificar(
    cedula_prueba,
    "Maria Isabel",
    "Gonzalez Gonzalez",
    "2003-05-20",
    "maria.isabel@gmail.com",
    "88887777",
    "Juan Ramirez",
    "87776655"
)


# Comprobar los cambios
print("\nDATOS DESPUES DE MODIFICAR")

estudiante = estudiantes.consultar(cedula_prueba)
print(estudiante)


# PRUEBA 5: ELIMINAR
print("\nPRUEBA 5: ELIMINAR")

estudiantes.eliminar(cedula_prueba)


# Comprobar que fue eliminado
print("\nDATOS DESPUES DE ELIMINAR")

estudiante = estudiantes.consultar(cedula_prueba)

if estudiante:
    print(estudiante)
else:
    print("El estudiante ya no existe en la base de datos.")