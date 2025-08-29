from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = "Usuario"
    ID_Usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Apellido = db.Column(db.String(100), nullable=False)
    Correo = db.Column(db.String(150), unique=True, nullable=False)
    Contrasena = db.Column(db.String(255), nullable=False)
    TipoDocumento = db.Column(db.String(50))
    NumeroDocumento = db.Column(db.String(50), unique=True)
    Direccion = db.Column(db.String(200))
    Telefono = db.Column(db.String(50))
    Estado = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    Calle = db.Column(db.String(100))
    Ciudad = db.Column(db.String(100))
    Departamento = db.Column(db.String(100))
    Genero = db.Column(db.Enum('M', 'F', 'Otro'))
    Rol = db.Column(db.Enum('Administrador','Docente','Estudiante','Acudiente'), nullable=False)

    matriculas = db.relationship("Matricula", back_populates="usuario")
    asignaturas = db.relationship("Asignatura", back_populates="usuario")
    programaciones = db.relationship("Programacion", back_populates="usuario")
    actividades = db.relationship("Actividad", back_populates="usuario")


class Matricula(db.Model):
    __tablename__ = "Matricula"
    ID_Matricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Estudiante = db.Column(db.Integer, db.ForeignKey("Usuario.ID_Usuario"), nullable=False)
    Correo = db.Column(db.String(150))
    FechaNacimiento = db.Column(db.Date)
    DepNacimiento = db.Column(db.String(100))
    TipoDocumento = db.Column(db.String(50))
    NumeroDocumento = db.Column(db.String(50))
    AnioLectivo = db.Column(db.String(4)) 

    usuario = db.relationship("Usuario", back_populates="matriculas")
    cursos = db.relationship("Curso", back_populates="matricula")
    observaciones = db.relationship("Observacion", back_populates="matricula")


class Curso(db.Model):
    __tablename__ = "Curso"
    ID_Curso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Grado = db.Column(db.String(10), nullable=False)
    Grupo = db.Column(db.String(10))
    Anio = db.Column(db.String(4), nullable=False)
    Estado = db.Column(db.Enum('Activo','Inactivo'), default='Activo')
    DirectorGrupo = db.Column(db.Integer)
    NumeroEstudiantes = db.Column(db.Integer)
    ID_Matricula = db.Column(db.Integer, db.ForeignKey("Matricula.ID_Matricula"))
    ID_Programacion = db.Column(db.Integer, db.ForeignKey("Programacion.ID_Programacion"))

    matricula = db.relationship("Matricula", back_populates="cursos")
    programacion = db.relationship("Programacion", back_populates="cursos")


class Asignatura(db.Model):
    __tablename__ = "Asignatura"
    ID_Asignatura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.Text)
    Grado = db.Column(db.String(10))
    Area = db.Column(db.String(100))
    CodigoAsignatura = db.Column(db.String(20), unique=True)
    Estado = db.Column(db.Enum('Activa','Inactiva'), default='Activa')
    ID_Usuario = db.Column(db.Integer, db.ForeignKey("Usuario.ID_Usuario"))
    ID_Programacion = db.Column(db.Integer, db.ForeignKey("Programacion.ID_Programacion"))

    usuario = db.relationship("Usuario", back_populates="asignaturas")
    programacion = db.relationship("Programacion", back_populates="asignaturas")


class Programacion(db.Model):
    __tablename__ = "Programacion"
    ID_Programacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Curso = db.Column(db.Integer, db.ForeignKey("Curso.ID_Curso"))
    ID_Asignatura = db.Column(db.Integer, db.ForeignKey("Asignatura.ID_Asignatura"))
    HoraInicio = db.Column(db.Time)
    HoraFin = db.Column(db.Time)
    Dia = db.Column(db.String(20))
    ID_Usuario = db.Column(db.Integer, db.ForeignKey("Usuario.ID_Usuario"))

    usuario = db.relationship("Usuario", back_populates="programaciones")
    cursos = db.relationship("Curso", back_populates="programacion")
    asignaturas = db.relationship("Asignatura", back_populates="programacion")
    asistencias = db.relationship("Asistencia", back_populates="programacion")
    observaciones = db.relationship("Observacion", back_populates="programacion")
    actividades = db.relationship("Actividad", back_populates="programacion")


class Asistencia(db.Model):
    __tablename__ = "Asistencia"
    ID_Asistencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fecha = db.Column(db.Date, nullable=False)
    ID_Estudiante = db.Column(db.Integer, db.ForeignKey("Usuario.ID_Usuario"))
    ID_Programacion = db.Column(db.Integer, db.ForeignKey("Programacion.ID_Programacion"))
    Estado = db.Column(db.Enum('Asistio','Falto'), nullable=False)
    Justificacion = db.Column(db.Text)

    programacion = db.relationship("Programacion", back_populates="asistencias")


class Observacion(db.Model):
    __tablename__ = "Observacion"
    ID_Observacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fecha = db.Column(db.Date, nullable=False)
    Descripcion = db.Column(db.Text)
    Tipo = db.Column(db.Enum('Academica','Convivencial'))
    NivelImportancia = db.Column(db.Enum('Bajo','Medio','Alto'))
    Recomendacion = db.Column(db.Text)
    Estado = db.Column(db.Enum('Activa','Inactiva'))
    ID_Programacion = db.Column(db.Integer, db.ForeignKey("Programacion.ID_Programacion"))
    ID_Matricula = db.Column(db.Integer, db.ForeignKey("Matricula.ID_Matricula"))

    programacion = db.relationship("Programacion", back_populates="observaciones")
    matricula = db.relationship("Matricula", back_populates="observaciones")


class Actividad(db.Model):
    __tablename__ = "Actividad"
    ID_Actividad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Titulo = db.Column(db.String(200), nullable=False)
    Tipo = db.Column(db.Enum('Taller','Examen','Participacion','Grupo'))
    Fecha = db.Column(db.Date)
    ID_Usuario = db.Column(db.Integer, db.ForeignKey("Usuario.ID_Usuario"))
    ID_Programacion = db.Column(db.Integer, db.ForeignKey("Programacion.ID_Programacion"))
    ID_Periodo = db.Column(db.Integer, db.ForeignKey("Periodo.ID_Periodo"))
    Estado = db.Column(db.Enum('Pendiente','Calificada','Cancelada'))
    Observacion = db.Column(db.Text)

    usuario = db.relationship("Usuario", back_populates="actividades")
    programacion = db.relationship("Programacion", back_populates="actividades")
    periodo = db.relationship("Periodo", back_populates="actividad")


class Periodo(db.Model):
    __tablename__ = "Periodo"
    ID_Periodo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NumeroPeriodo = db.Column(db.Integer, nullable=False)
    Anio = db.Column(db.String(4), nullable=False)
    FechaInicial = db.Column(db.Date)
    FechaFinal = db.Column(db.Date)
    Porcentaje = db.Column(db.Numeric(5,2))
    NotaFinal = db.Column(db.Numeric(5,2))
    ID_Actividad = db.Column(db.Integer, db.ForeignKey("Actividad.ID_Actividad"))

    actividad = db.relationship("Actividad", back_populates="periodo")