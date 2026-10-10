/*Creacion de la base de datos*/

CREATE DATABASE ControlAcademico;
GO

USE ControlAcademicoDB;
GO


/*Tabla estudiantes */

CREATE TABLE Estudiantes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cedula VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    correo VARCHAR(100),
    celular VARCHAR(15),
    nombre_encargado VARCHAR(100),
    celular_encargado VARCHAR(15)
);
GO


/* Tabla cursos */

CREATE TABLE Cursos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    referencia VARCHAR(35) NOT NULL UNIQUE,
    descripcion VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_final DATE NOT NULL,
    estado NUMERIC(1) NOT NULL,
    docente VARCHAR(30),
    horas_capacitacion INT,
    horas_asesoria DECIMAL(10,2),
    mes VARCHAR(20)
);
GO


/* Tabla matriculas*/

CREATE TABLE Matriculas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cedula INT NOT NULL,
    referencia INT NOT NULL,
    fecha_matricula DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,

    CONSTRAINT FK_Matriculas_Estudiantes
        FOREIGN KEY (cedula)
        REFERENCES Estudiantes(id),

    CONSTRAINT FK_Matriculas_Cursos
        FOREIGN KEY (referencia)
        REFERENCES Cursos(id)
);
GO


/*Tabla de asistencias*/

CREATE TABLE Asistencias (
    id INT IDENTITY(1,1) PRIMARY KEY,
    matricula_id INT NOT NULL,
    fecha DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,

    CONSTRAINT FK_Asistencias_Matriculas
        FOREIGN KEY (matricula_id)
        REFERENCES Matriculas(id),

    CONSTRAINT UQ_Asistencia_Matricula_Fecha
        UNIQUE (matricula_id, fecha)
);
GO


/*Tabla dias no laborados*/

CREATE TABLE Dias_No_Laborados (
    id INT IDENTITY(1,1) PRIMARY KEY,
    curso_id INT NOT NULL,
    fecha DATE NOT NULL,
    codigo VARCHAR(5) NOT NULL,

    CONSTRAINT FK_DiasNoLaborados_Cursos
        FOREIGN KEY (curso_id)
        REFERENCES Cursos(id)
);
GO
