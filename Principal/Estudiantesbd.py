import re
from datetime import datetime
from Conexion import conectar


class Estudiantes:
    def __init__(self):
        self.mensaje_error = ""
 
    def validar_datos(
        self, cedula, nombre, apellidos, fecha_nacimiento,
        correo, celular, nombre_encargado, celular_encargado
    ):
        # Cédula obligatoria y solo números
        if not cedula or not cedula.isdigit():
            self.mensaje_error = "La cédula es obligatoria y debe contener solo números."
            return False
 
        # Nombre y apellidos obligatorios
        if not nombre.strip():
            self.mensaje_error = "El nombre es obligatorio."
            return False
 
        if not apellidos.strip():
            self.mensaje_error = "Los apellidos son obligatorios."
            return False
 
        # Revisar que la fecha tenga el formato que usa la base de datos
        try:
            datetime.strptime(str(fecha_nacimiento), "%Y-%m-%d")
        except ValueError:
            self.mensaje_error = "La fecha de nacimiento debe tener el formato AAAA-MM-DD."
            return False
 
        # El correo puede quedar vacío, pero si se escribe debe ser válido
        if correo and not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", correo):
            self.mensaje_error = "El correo electrónico no tiene un formato válido."
            return False
 
        # Los teléfonos son opcionales, pero solo pueden contener números
        if celular and not celular.isdigit():
            self.mensaje_error = "El celular del estudiante debe contener solo números."
            return False
 
        if celular_encargado and not celular_encargado.isdigit():
            self.mensaje_error = "El celular del encargado debe contener solo números."
            return False
 
        # Verificar que la cédula no esté registrada por otro estudiante
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM Estudiantes WHERE cedula = ?",
                (cedula,)
            )
            existe = cursor.fetchone()[0] > 0
 
            if existe:
                self.mensaje_error = "Ya existe un estudiante registrado con esa cédula."
                return False
 
            return True
 
        finally:
            if conexion is not None:
                conexion.close()
 
    def registrar(
        self, cedula, nombre, apellidos, fecha_nacimiento,
        correo, celular, nombre_encargado, celular_encargado
    ):
        if not self.validar_datos(
            cedula, nombre, apellidos, fecha_nacimiento,
            correo, celular, nombre_encargado, celular_encargado
        ):
            raise ValueError(self.mensaje_error)
 
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO Estudiantes
                    (cedula, nombre, apellidos, fecha_nacimiento, correo,
                     celular, nombre_encargado, celular_encargado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cedula, nombre, apellidos, fecha_nacimiento,
                correo or None, celular or None,
                nombre_encargado or None, celular_encargado or None
            ))
            conexion.commit()
        finally:
            if conexion is not None:
                conexion.close()
 
    def listar(self):
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, cedula, nombre, apellidos, fecha_nacimiento,
                       correo, celular, nombre_encargado, celular_encargado
                FROM Estudiantes
                ORDER BY id
            """)
            return cursor.fetchall()
        finally:
            if conexion is not None:
                conexion.close()
 
    def consultar(self, cedula):
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, cedula, nombre, apellidos, fecha_nacimiento,
                       correo, celular, nombre_encargado, celular_encargado
                FROM Estudiantes
                WHERE cedula = ?
            """, (cedula,))
            return cursor.fetchone()
        finally:
            if conexion is not None:
                conexion.close()
 
    def modificar(
        self, cedula, nombre, apellidos, fecha_nacimiento,
        correo, celular, nombre_encargado, celular_encargado
    ):
        # No se cambia la cédula; se utiliza para localizar el estudiante
        # que se seleccionó en la tabla.
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
 
            cursor.execute(
                "SELECT COUNT(*) FROM Estudiantes WHERE cedula = ?",
                (cedula,)
            )
            if cursor.fetchone()[0] == 0:
                raise ValueError("No se encontró un estudiante con esa cédula.")
 
            # Validaciones de los datos editables
            if not nombre.strip():
                raise ValueError("El nombre es obligatorio.")
            if not apellidos.strip():
                raise ValueError("Los apellidos son obligatorios.")
            try:
                datetime.strptime(str(fecha_nacimiento), "%Y-%m-%d")
            except ValueError:
                raise ValueError("La fecha de nacimiento debe tener el formato AAAA-MM-DD.")
            if correo and not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", correo):
                raise ValueError("El correo electrónico no tiene un formato válido.")
            if celular and not celular.isdigit():
                raise ValueError("El celular del estudiante debe contener solo números.")
            if celular_encargado and not celular_encargado.isdigit():
                raise ValueError("El celular del encargado debe contener solo números.")
 
            cursor.execute("""
                UPDATE Estudiantes
                SET nombre = ?, apellidos = ?, fecha_nacimiento = ?, correo = ?,
                    celular = ?, nombre_encargado = ?, celular_encargado = ?
                WHERE cedula = ?
            """, (
                nombre, apellidos, fecha_nacimiento, correo or None,
                celular or None, nombre_encargado or None,
                celular_encargado or None, cedula
            ))
            conexion.commit()
        finally:
            if conexion is not None:
                conexion.close()
 
    def eliminar(self, cedula):
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Estudiantes WHERE cedula = ?", (cedula,))
            if cursor.rowcount == 0:
                raise ValueError("No se encontró un estudiante con esa cédula.")
            conexion.commit()
        finally:
            if conexion is not None:
                conexion.close()
 
    def contar_matriculas(self, cedula):
        # Cuantas matriculas tiene el estudiante (se borran al eliminarlo)
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM Matriculas m
                INNER JOIN Estudiantes e ON m.estudiante_id = e.id
                WHERE e.cedula = ?
            """, (cedula,))
            return cursor.fetchone()[0]
        finally:
            if conexion is not None:
                conexion.close()
