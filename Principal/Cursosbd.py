from datetime import datetime
from Conexion import conectar
 
 
class Cursos:
    def __init__(self):
        self.mensaje_error = ""
 
    # Convierte el texto de estado de la pantalla a 1 o 0 para la base de datos
    def estado_a_numero(self, estado):
        if str(estado).strip().lower() in ("1", "activo"):
            return 1
        return 0
 
    # Convierte el 1 o 0 de la base de datos a texto para mostrar en la tabla
    def estado_a_texto(self, estado):
        return "Activo" if str(estado) in ("1", "True") else "Inactivo"
 
    def validar_campos(
        self, referencia, descripcion, fecha_inicio, fecha_final,
        docente, horas_capacitacion, horas_asesoria, mes
    ):
        # Esta validación se usa tanto al guardar como al actualizar
        # Devuelve True si todo está bien, o False con el mensaje en mensaje_error
 
        # Referencia obligatoria
        if not referencia.strip():
            self.mensaje_error = "La referencia es obligatoria."
            return False
 
        if len(referencia.strip()) > 35:
            self.mensaje_error = "La referencia no puede tener más de 35 caracteres."
            return False
 
        # Descripción obligatoria
        if not descripcion.strip():
            self.mensaje_error = "La descripción es obligatoria."
            return False
 
        if len(descripcion.strip()) > 100:
            self.mensaje_error = "La descripción no puede tener más de 100 caracteres."
            return False
 
        # Las fechas deben tener el formato que usa la base de datos
        try:
            inicio = datetime.strptime(str(fecha_inicio), "%Y-%m-%d")
        except ValueError:
            self.mensaje_error = "La fecha de inicio debe tener el formato AAAA-MM-DD."
            return False
 
        try:
            final = datetime.strptime(str(fecha_final), "%Y-%m-%d")
        except ValueError:
            self.mensaje_error = "La fecha final debe tener el formato AAAA-MM-DD."
            return False
 
        # La fecha final debe ser mayor o igual a la fecha de inicio
        if final < inicio:
            self.mensaje_error = "La fecha final debe ser mayor o igual a la fecha de inicio."
            return False
 
        # El docente es opcional, pero tiene un máximo de caracteres
        if docente and len(docente.strip()) > 30:
            self.mensaje_error = "El nombre del docente no puede tener más de 30 caracteres."
            return False
 
        # Las horas de capacitación son opcionales, pero deben ser enteras
        if horas_capacitacion and not str(horas_capacitacion).strip().isdigit():
            self.mensaje_error = "Las horas de capacitación deben ser un número entero."
            return False
 
        # Las horas de asesoría son opcionales, pero deben ser decimales
        if horas_asesoria:
            try:
                valor = float(str(horas_asesoria).strip().replace(",", "."))
            except ValueError:
                self.mensaje_error = "Las horas de asesoría deben ser un número decimal (por ejemplo 8.5)."
                return False
 
            if valor < 0:
                self.mensaje_error = "Las horas de asesoría no pueden ser negativas."
                return False
 
        # El mes es opcional, pero tiene un máximo de caracteres
        if mes and len(mes.strip()) > 20:
            self.mensaje_error = "El mes no puede tener más de 20 caracteres."
            return False
 
        return True
 
    def validar_datos(
        self, referencia, descripcion, fecha_inicio, fecha_final, estado,
        docente, horas_capacitacion, horas_asesoria, mes
    ):
        # Validaciones generales
        if not self.validar_campos(
            referencia, descripcion, fecha_inicio, fecha_final,
            docente, horas_capacitacion, horas_asesoria, mes
        ):
            return False
 
        # Verificar que la referencia no esté registrada en otro curso
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM Cursos WHERE referencia = ?",
                (referencia.strip(),)
            )
            existe = cursor.fetchone()[0] > 0
 
            if existe:
                self.mensaje_error = "Ya existe un curso registrado con esa referencia."
                return False
 
            return True
 
        finally:
            if conexion is not None:
                conexion.close()
 
    def registrar(
        self, referencia, descripcion, fecha_inicio, fecha_final, estado,
        docente, horas_capacitacion, horas_asesoria, mes
    ):
        if not self.validar_datos(
            referencia, descripcion, fecha_inicio, fecha_final, estado,
            docente, horas_capacitacion, horas_asesoria, mes
        ):
            raise ValueError(self.mensaje_error)
 
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO Cursos
                    (referencia, descripcion, fecha_inicio, fecha_final, estado,
                     docente, horas_capacitacion, horas_asesoria, mes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                referencia.strip(), descripcion.strip(), fecha_inicio, fecha_final,
                self.estado_a_numero(estado),
                docente.strip() or None,
                int(horas_capacitacion) if horas_capacitacion else None,
                float(str(horas_asesoria).replace(",", ".")) if horas_asesoria else None,
                mes.strip() or None
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
                SELECT id, referencia, descripcion, fecha_inicio, fecha_final,
                       estado, docente, horas_capacitacion, horas_asesoria, mes
                FROM Cursos
                ORDER BY id
            """)
            return cursor.fetchall()
        finally:
            if conexion is not None:
                conexion.close()
 
    def consultar(self, referencia):
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, referencia, descripcion, fecha_inicio, fecha_final,
                       estado, docente, horas_capacitacion, horas_asesoria, mes
                FROM Cursos
                WHERE referencia = ?
            """, (referencia,))
            return cursor.fetchone()
        finally:
            if conexion is not None:
                conexion.close()
 
    def modificar(
        self, referencia, descripcion, fecha_inicio, fecha_final, estado,
        docente, horas_capacitacion, horas_asesoria, mes
    ):
        # No se cambia la referencia; se utiliza para localizar el curso
        # que se seleccionó en la tabla.
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
 
            cursor.execute(
                "SELECT COUNT(*) FROM Cursos WHERE referencia = ?",
                (referencia,)
            )
            if cursor.fetchone()[0] == 0:
                raise ValueError("No se encontró un curso con esa referencia.")
 
            # Validaciones de los datos editables
            if not self.validar_campos(
                referencia, descripcion, fecha_inicio, fecha_final,
                docente, horas_capacitacion, horas_asesoria, mes
            ):
                raise ValueError(self.mensaje_error)
 
            cursor.execute("""
                UPDATE Cursos
                SET descripcion = ?, fecha_inicio = ?, fecha_final = ?, estado = ?,
                    docente = ?, horas_capacitacion = ?, horas_asesoria = ?, mes = ?
                WHERE referencia = ?
            """, (
                descripcion.strip(), fecha_inicio, fecha_final,
                self.estado_a_numero(estado),
                docente.strip() or None,
                int(horas_capacitacion) if horas_capacitacion else None,
                float(str(horas_asesoria).replace(",", ".")) if horas_asesoria else None,
                mes.strip() or None,
                referencia
            ))
            conexion.commit()
        finally:
            if conexion is not None:
                conexion.close()
 
    def eliminar(self, referencia):
        # Si el curso tiene matriculas o dias no laborados, la base de datos
        # no deja eliminarlo y lanza pyodbc.IntegrityError.
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Cursos WHERE referencia = ?", (referencia,))
            if cursor.rowcount == 0:
                raise ValueError("No se encontró un curso con esa referencia.")
            conexion.commit()
        finally:
            if conexion is not None:
                conexion.close()
 