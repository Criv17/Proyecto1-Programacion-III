USE ControlAcademico
/* DATOS DE ESTUDIANTES */

INSERT INTO Estudiantes
(cedula, nombre, apellidos, fecha_nacimiento, correo, celular,
 nombre_encargado, celular_encargado)
VALUES
('301780456', 'María', 'González Gomez', '2004-05-18',
 'maria.gonzalez@gmail.com', '88881234',
 'Laura Rodríguez', '87772345'),

('304560789', 'Kevin', 'Rodríguez Vargas', '2003-11-22',
 'kevin.rodriguez@gmail.com', '88994567',
 'Carlos Vargas', '86663456'),

('112340678', 'Daniel', 'Valverde Solano', '2005-02-10',
 'daniel.valverde@gmail.com', '87776789',
 'Ana Solano', '85554567'),

('209870345', 'Sofía', 'Mora Jiménez', '2004-08-30',
 'sofia.mora@gmail.com', '86667890',
 'Patricia Jiménez', '84445678'),

('315670890', 'Andrés', 'Ceciliano Pérez', '2003-12-14',
 'andres.ceciliano@gmail.com', '85558901',
 'Luis Pérez', '83336789');
GO


/* DATOS DE CURSOS */

INSERT INTO Cursos
(referencia, descripcion, fecha_inicio, fecha_final, estado,
 docente, horas_capacitacion, horas_asesoria, mes)
VALUES
('TI-142', 'Fundamentos de Base de Datos',
 '2026-05-04', '2026-08-22', 1,
 'Carlomagno', 64, 10.00, 'Mayo'),

('TI-143', 'Programación',
 '2026-05-05', '2026-08-23', 1,
 'Carlos Mora', 64, 8.00, 'Mayo'),

('TI-144', 'Sistemas Operativos',
 '2026-05-06', '2026-08-24', 1,
 'Ana Rodríguez', 48, 6.00, 'Mayo'),

('TI-145', 'Redes de Computadoras',
 '2026-05-07', '2026-08-25', 1,
 'Luis Vargas', 64, 8.00, 'Mayo'),

('TI-146', 'Análisis de Sistemas',
 '2026-05-08', '2026-08-26', 1,
 'María Solano', 48, 6.00, 'Mayo');
GO


/* DATOS DE MATRICULAS */

INSERT INTO Matriculas
(cedula, referencia, fecha_matricula, estado)
VALUES
(1, 1, '2026-04-20', 'Activa'),
(2, 1, '2026-04-21', 'Activa'),
(3, 2, '2026-04-21', 'Activa'),
(4, 3, '2026-04-22', 'Activa'),
(5, 4, '2026-04-22', 'Activa'),
(1, 5, '2026-04-23', 'Activa');
GO


/* DATOS DE ASISTENCIAS */

INSERT INTO Asistencias
(matricula_id, fecha, estado)
VALUES
(1, '2026-05-05', 'Presente'),
(1, '2026-05-12', 'Presente'),
(1, '2026-05-19', 'Ausente'),

(2, '2026-05-05', 'Presente'),
(2, '2026-05-12', 'Tarde'),
(2, '2026-05-19', 'Presente'),

(3, '2026-05-06', 'Presente'),
(3, '2026-05-13', 'Ausente'),

(4, '2026-05-07', 'Presente'),
(4, '2026-05-14', 'Presente'),

(5, '2026-05-08', 'Tarde'),
(5, '2026-05-15', 'Presente'),

(6, '2026-05-08', 'Presente');
GO


/* DATOS DE DIAS NO LABORADO */

INSERT INTO Dias_No_Laborados
(curso_id, fecha, codigo)
VALUES
(1, '2026-07-25', 'FERIA'),
(1, '2026-08-02', 'FERIA'),
(2, '2026-07-25', 'FERIA'),
(3, '2026-08-02', 'FERIA'),
(4, '2026-07-25', 'FERIA');
GO


/* CONSULTAS PARA COMPROBAR QUE TODO FUNCIONA */

SELECT * FROM Estudiantes;

SELECT * FROM Cursos;

SELECT * FROM Matriculas;

SELECT * FROM Asistencias;

SELECT * FROM Dias_No_Laborados;
GO