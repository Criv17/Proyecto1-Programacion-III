import re
from datetime import datetime
from Conexion import conectar


class Cursos:
    # Valores de referencia para las validaciones
    MESES = (
        "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
        "agosto", "setiembre", "septiembre", "octubre", "noviembre", "diciembre"
    )
    ESTADOS = ("activo", "inactivo")
    HORAS_MAXIMAS = 1000
    ANIO_MINIMO = 2000
    ANIO_MAXIMO = 2100

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
        self, referencia, descripcion, fecha_inicio, fecha_final, estado,
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

        # La referencia solo puede tener letras, números, espacios, guiones y puntos
        if not re.fullmatch(r"[A-Za-z0-9 ._\-]+", referencia.strip()):
            self.mensaje_error = "La referencia solo puede tener letras, números, espacios, guiones y puntos."
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

        # Los años deben estar en un rango razonable
        for fecha, nombre in ((inicio, "inicio"), (final, "final")):
            if fecha.year < self.ANIO_MINIMO or fecha.year > self.ANIO_MAXIMO:
                self.mensaje_error = (
                    f"El año de la fecha de {nombre} debe estar entre "
                    f"{self.ANIO_MINIMO} y {self.ANIO_MAXIMO}."
                )
                return False

        # La fecha final debe ser mayor o igual a la fecha de inicio
        if final < inicio:
            self.mensaje_error = "La fecha final debe ser mayor o igual a la fecha de inicio."
            return False

        # El estado solo puede ser Activo o Inactivo
        if str(estado).strip().lower() not in self.ESTADOS:
            self.mensaje_error = "El estado debe ser Activo o Inactivo."
            return False

        # El docente es opcional, pero tiene un máximo de caracteres
        if docente and len(docente.strip()) > 30:
            self.mensaje_error = "El nombre del docente no puede tener más de 30 caracteres."
            return False

        # El docente solo puede tener letras, espacios, puntos, apóstrofes y guiones
        if docente and not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ .'\-]+", docente.strip()):
            self.mensaje_error = "El nombre del docente solo puede tener letras y espacios."
            return False

        # Las horas de capacitación son opcionales, pero deben ser enteras
        if horas_capacitacion:
            if not re.fullmatch(r"[0-9]+", str(horas_capacitacion).strip()):
                self.mensaje_error = "Las horas de capacitación deben ser un número entero."
                return False

            if int(horas_capacitacion) > self.HORAS_MAXIMAS:
                self.mensaje_error = f"Las horas de capacitación no pueden ser mayores a {self.HORAS_MAXIMAS}."
                return False

        # Las horas de asesoría son opcionales, pero deben ser decimales
        # positivos con un máximo de 2 decimales (así los guarda la base de datos)
        if horas_asesoria:
            if not re.fullmatch(r"[0-9]+([.,][0-9]{1,2})?", str(horas_asesoria).strip()):
                self.mensaje_error = (
                    "Las horas de asesoría deben ser un número decimal positivo "
                    "con máximo 2 decimales (por ejemplo 8.5)."
                )
                return False

            valor = float(str(horas_asesoria).strip().replace(",", "."))

            if valor > self.HORAS_MAXIMAS:
                self.mensaje_error = f"Las horas de asesoría no pueden ser mayores a {self.HORAS_MAXIMAS}."
                return False

        # El mes es opcional, pero si se escribe debe ser un mes válido
        if mes:
            if len(mes.strip()) > 20:
                self.mensaje_error = "El mes no puede tener más de 20 caracteres."
                return False

            if mes.strip().lower() not in self.MESES:
                self.mensaje_error = "El mes debe ser un nombre de mes válido (por ejemplo Mayo)."
                return False

        return True

    def validar_datos(
        self, referencia, descripcion, fecha_inicio, fecha_final, estado,
        docente, horas_capacitacion, horas_asesoria, mes
    ):
        # Validaciones generales
        if not self.validar_campos(
            referencia, descripcion, fecha_inicio, fecha_final, estado,
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
                referencia, descripcion, fecha_inicio, fecha_final, estado,
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

    def contar_matriculas(self, referencia):
        # Cuantas matriculas tiene el curso (se borran al eliminarlo)
        conexion = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM Matriculas m
                INNER JOIN Cursos c ON m.curso_id = c.id
                WHERE c.referencia = ?
            """, (referencia,))
            return cursor.fetchone()[0]
        finally:
            if conexion is not None:
                conexion.close()

    def eliminar(self, referencia):
        # Las matrículas y los días no laborados del curso se borran solos
        # por el ON DELETE CASCADE de la base de datos.
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