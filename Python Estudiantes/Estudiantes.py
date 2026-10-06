from ConexionSQL import conectar


class Estudiantes:

    # Se crea un metodo que registra un nuevo estudiante
    def registrar(self, cedula, nombre, apellidos, fecha_nacimiento,
                  correo, celular, nombre_encargado, celular_encargado):

        # Crear la conexion con la base de datos
        conexion = conectar()

        # Crear el cursor para ejecutar instrucciones SQL
        cursor = conexion.cursor()

        # Instruccion para insertar el estudiante
        sql = """
        INSERT INTO Estudiantes
        (cedula, nombre, apellidos, fecha_nacimiento, correo, celular,
        nombre_encargado, celular_encargado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Ejecutar la instruccion con los datos del estudiante
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

        # Guardar los cambios en la base de datos
        conexion.commit()

        # Cerrar la conexion
        conexion.close()

        print("Estudiante registrado correctamente.")

    # Metodo que muestra todos los estudiantes registrados
    def listar(self):

        # Crear la conexion con la base de datos
        conexion = conectar()

        # Crear el cursor para ejecutar instrucciones SQL
        cursor = conexion.cursor()

        # Consultar todos los estudiantes
        cursor.execute("SELECT * FROM Estudiantes")

        # Obtener todos los resultados
        estudiantes = cursor.fetchall()

        # Cerrar la conexion
        conexion.close()

        # Devolver la lista de estudiantes
        return estudiantes