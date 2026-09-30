ALTER TABLE Matriculas
DROP CONSTRAINT FK_Matriculas_Estudiantes;
GO

ALTER TABLE Matriculas
ADD CONSTRAINT FK_Matriculas_Estudiantes
FOREIGN KEY (cedula)
REFERENCES Estudiantes(id)
ON DELETE CASCADE;
GO