
# Importar herramientas para validar los datos
import re
from datetime import datetime

# Importar la funcion que conecta con SQL Server
from ConexionSQL import conectar


# Clase que contiene las operaciones de estudiantes
class Estudiantes:

    # Validar los datos antes de registrar o modificar
    def validar_datos(self, cedula, nombre, apellidos, fecha_nacimiento,
                      correo, celular, nombre_encargado, celular_encargado,
                      cedula_original=None):

        # Validar y Comprobar que la cedula no este vacia
        if not cedula or not cedula.strip():
            print("Error: La cedula es obligatoria.")
            return False

        # Comprobar que la cedula tenga solamente numeros
        if not cedula.isdigit():
            print("Error: La cedula debe contener solo numeros.")
            return False

        # Validar que el nombre no este vacio
        if not nombre or not nombre.strip():
            print("Error: El nombre es obligatorio.")
            return False

        # Validar que los apellidos no esten vacios
        if not apellidos or not apellidos.strip():
            print("Error: Los apellidos son obligatorios.")
            return False

        # Validar que la fecha tenga el formato AAAA-MM-DD
        try:
            datetime.strptime(str(fecha_nacimiento), "%Y-%m-%d")
        except (ValueError, TypeError):
            print("Error: La fecha debe tener el formato AAAA-MM-DD.") # comprobar que la fecha de nacimiento tenga el formato correcto, representan el formato esperado 
            return False

        # Comprobar el formato del correo si se escribio uno
        if correo and correo.strip():
            patron_correo = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

            if not re.match(patron_correo, correo.strip()):
                print("Error: El correo brindado no tiene un formato valido, compruebe y vuelva a intentarlo")
                return False

        # Comprobar que el celular del estudiante tenga solo numeros
        if celular and celular.strip():
            if not celular.isdigit():
                print("Error: El telefono debe tener solo numeros.")
                return False

        # Comprobar que el celular del encargado tenga solo numeros
        if celular_encargado and celular_encargado.strip():
            if not celular_encargado.isdigit():
                print("Error: El numero de telegono del encargado debe tener solo numeros")
                return False

        # Conectarse a la base de datos para revisar la cedula
        conexion = conectar()
        cursor = conexion.cursor()

        # Buscar si ya existe un estudiante con esa cedula
        cursor.execute(
            "SELECT cedula FROM Estudiantes WHERE cedula = ?",
            (cedula,)
        )

        # Guardar el resultado de la busqueda
        estudiante = cursor.fetchone()

        # Cerrar la conexion porque ya se hizo la consulta
        conexion.close()

        # Si la cedula ya existe, impedir el registro duplicado
        # Al modificar, se permite conservar la cedula actual
        if estudiante and cedula != cedula_original:
            print("Error: Ya existe un estudiante con esa cedula.")
            return False

        # Si ninguna validacion fallo, los datos son validos
        return True

    # Registrar un estudiante nuevo en la base de datos
    def registrar(self, cedula, nombre, apellidos, fecha_nacimiento,
                  correo, celular, nombre_encargado, celular_encargado):

        # Validar los datos antes de intentar guardarlos
        if not self.validar_datos(
            cedula, nombre, apellidos, fecha_nacimiento,
            correo, celular, nombre_encargado, celular_encargado
        ):
            # Si los datos son incorrectos, detener el registro
            return

        # Abrir la conexion con SQL Server
        conexion = conectar()

        # Crear el cursor para ejecutar instrucciones SQL
        cursor = conexion.cursor()

        # Preparar la instruccion para insertar un estudiante
        # Los signos ? se reemplazan por los valores enviados
        sql = """
        INSERT INTO Estudiantes
        (cedula, nombre, apellidos, fecha_nacimiento, correo, celular,
        nombre_encargado, celular_encargado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Ejecutar la instruccion con los datos recibidos
        cursor.execute(sql, (
            cedula,
            nombre,
            apellidos,
            fecha_nacimiento,
            correo,
            celular,
            nombre_encargado,
            celular_encargado
        ))

        # Guardar definitivamente los cambios en la base de datos
        conexion.commit()

        # Cerrar la conexion para liberar recursos
        conexion.close()

        # Informar que el registro termino correctamente
        print("Estudiante registrado correctamente.")

    # Consultar y mostrar todos los estudiantes registrados
    def listar(self):

        conexion = conectar() # Conectarse a la base de datos
        cursor = conexion.cursor()

        # Seleccionar todos los registros de la tabla Estudiantes
        cursor.execute("SELECT * FROM Estudiantes")

        # Obtener todas las filas encontradas
        estudiantes = cursor.fetchall()

        # Cerrar la conexion
        conexion.close()

        # Devolver la lista para que otra parte del programa la use
        return estudiantes

    # Buscar un estudiante utilizando su cedula
    def consultar(self, cedula):

        # Conectarse a la base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        # Buscar solamente al estudiante con la cedula indicada
        cursor.execute(
            "SELECT * FROM Estudiantes WHERE cedula = ?",
            (cedula,)
        )

        # Obtener una sola fila; devuelve None si no existe
        estudiante = cursor.fetchone()

        # Cerrar la conexion
        conexion.close()

        # Devolver los datos encontrados
        return estudiante

    # Modificar los datos de algun estudiante de la DB
    def modificar(self, cedula, nombre, apellidos, fecha_nacimiento,
                  correo, celular, nombre_encargado, celular_encargado):

        # Validar los nuevos datos antes de guardarlos
        # cedula_original permite conservar la cedula actual
        if not self.validar_datos(
            cedula, nombre, apellidos, fecha_nacimiento,
            correo, celular, nombre_encargado, celular_encargado,
            cedula_original=cedula
        ):
            return #simplemente se asegura que se cumplan las validaciones 

        # Conectarse a la base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        # Preparar la instruccion que actualiza los datos
        # WHERE indica cual estudiante se debe modificar
        sql = """
        UPDATE Estudiantes
        SET nombre = ?, apellidos = ?, fecha_nacimiento = ?,
            correo = ?, celular = ?, nombre_encargado = ?,
            celular_encargado = ?
        WHERE cedula = ?
        """

        # Ejecutar la modificacion con los nuevos valores
        cursor.execute(sql, (
            nombre,
            apellidos,
            fecha_nacimiento,
            correo,
            celular,
            nombre_encargado,
            celular_encargado,
            cedula
        ))

        # Guardar los cambios
        conexion.commit()

        # Revisar si se modifico algun registro
        if cursor.rowcount > 0:
            print("Estudiante modificado correctamente.")
        else:
            print("No se encontro un estudiante con esa cedula.")

        # Cerrar la conexion
        conexion.close()

    # Eliminar un estudiante utilizando su cedula
    def eliminar(self, cedula):

        # Conectarse a la base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        # Eliminar solamente al estudiante que tenga esa cedula
        cursor.execute(
            "DELETE FROM Estudiantes WHERE cedula = ?",
            (cedula,)
        )

        # Guardar los cambios en la base de datos
        conexion.commit()

        # Comprobar si se elimino algun registro
        if cursor.rowcount > 0:
            print("Estudiante eliminado correctamente.")
        else:
            print("No se encontro un estudiante con esa cedula.")

        # Cerrar la conexion
        conexion.close()
