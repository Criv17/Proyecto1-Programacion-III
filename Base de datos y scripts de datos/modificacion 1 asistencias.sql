use ControlAcademico
--modificacion a tabla asistencias

ALTER TABLE Asistencias
DROP CONSTRAINT FK_Asistencias_Matriculas;
GO

ALTER TABLE Asistencias
ADD CONSTRAINT FK_Asistencias_Matriculas
FOREIGN KEY (matricula_id)
REFERENCES Matriculas(id)
ON DELETE CASCADE;
GO
