from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Enum, Text, ForeignKey, DECIMAL, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import YEAR

db = SQLAlchemy()

# Definir las clases para cada tabla. El orden es crucial para evitar errores de clave foránea.
# Las tablas sin dependencias se definen primero.
class Usuario(db.Model):
    __tablename__ = 'Usuario'
    ID_Usuario = db.Column(Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(String(100), nullable=False)
    Apellido = db.Column(String(100), nullable=False)
    Correo = db.Column(String(150), unique=True, nullable=False)
    Contrasena = db.Column(String(255), nullable=False)
    TipoDocumento = db.Column(String(50))
    NumeroDocumento = db.Column(String(50), unique=True)
    Direccion = db.Column(String(200))
    Telefono = db.Column(String(50))
    Estado = db.Column(Enum('Activo', 'Inactivo'), default='Activo')
    Calle = db.Column(String(100))
    Ciudad = db.Column(String(100))
    Departamento = db.Column(String(100))
    Genero = db.Column(Enum('M', 'F', 'Otro'))
    Rol = db.Column(Enum('Administrador', 'Docente', 'Estudiante', 'Acudiente'), nullable=False)

    # Relaciones inversas
    matriculas = relationship('Matricula', backref='usuario', lazy=True)
    programaciones_docente = relationship('Programacion', backref='docente', lazy=True, foreign_keys='Programacion.ID_Usuario')
    asistencias = relationship('Asistencia', backref='estudiante', lazy=True)
    actividades = relationship('Actividad', backref='usuario_actividad', lazy=True)
    asignaturas = relationship('Asignatura', backref='usuario_asignatura', lazy=True)


class Matricula(db.Model):
    __tablename__ = 'Matricula'
    ID_Matricula = db.Column(Integer, primary_key=True, autoincrement=True)
    ID_Estudiante = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'), nullable=False)
    Correo = db.Column(String(150))
    FechaNacimiento = db.Column(Date)
    DepNacimiento = db.Column(String(100))
    TipoDocumento = db.Column(String(50))
    NumeroDocumento = db.Column(String(50))
    AnioLectivo = db.Column(YEAR)

    # Relaciones inversas
    cursos = relationship('Curso', backref='matricula', lazy=True)
    observaciones = relationship('Observacion', backref='matricula', lazy=True)

class Periodo(db.Model):
    __tablename__ = 'Periodo'
    ID_Periodo = db.Column(Integer, primary_key=True, autoincrement=True)
    NumeroPeriodo = db.Column(Integer, nullable=False)
    Anio = db.Column(YEAR, nullable=False)
    FechaInicial = db.Column(Date)
    FechaFinal = db.Column(Date)
    Porcentaje = db.Column(DECIMAL(5, 2))
    NotaFinal = db.Column(DECIMAL(5, 2))
    ID_Actividad = db.Column(Integer, ForeignKey('Actividad.ID_Actividad'))

    # Relación inversa
    actividades = relationship('Actividad', backref='periodo', lazy=True)

# Las tablas con dependencias circulares se crean después de que todas las demás se hayan definido.
# Se usa `forward references` con el nombre de la tabla como string.
class Programacion(db.Model):
    __tablename__ = 'Programacion'
    ID_Programacion = db.Column(Integer, primary_key=True, autoincrement=True)
    ID_Curso = db.Column(Integer, ForeignKey('Curso.ID_Curso'))
    ID_Asignatura = db.Column(Integer, ForeignKey('Asignatura.ID_Asignatura'))
    HoraInicio = db.Column(Time)
    HoraFin = db.Column(Time)
    Dia = db.Column(String(20))
    ID_Usuario = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'))

    # Relaciones inversas
    cursos_programacion = relationship('Curso', backref='programacion', lazy=True, foreign_keys='Programacion.ID_Curso')
    asignaturas_programacion = relationship('Asignatura', backref='programacion_asignatura', lazy=True, foreign_keys='Programacion.ID_Asignatura')
    asistencias = relationship('Asistencia', backref='programacion_asistencia', lazy=True)
    observaciones = relationship('Observacion', backref='programacion_observacion', lazy=True)
    actividades = relationship('Actividad', backref='programacion_actividad', lazy=True)

class Curso(db.Model):
    __tablename__ = 'Curso'
    ID_Curso = db.Column(Integer, primary_key=True, autoincrement=True)
    Grado = db.Column(String(10), nullable=False)
    Grupo = db.Column(String(10))
    Anio = db.Column(YEAR, nullable=False)
    Estado = db.Column(Enum('Activo', 'Inactivo'), default='Activo')
    DirectorGrupo = db.Column(Integer)
    NumeroEstudiantes = db.Column(Integer)
    ID_Matricula = db.Column(Integer, ForeignKey('Matricula.ID_Matricula'))
    ID_Programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))

class Asignatura(db.Model):
    __tablename__ = 'Asignatura'
    ID_Asignatura = db.Column(Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(String(100), nullable=False)
    Descripcion = db.Column(Text)
    Grado = db.Column(String(10))
    Area = db.Column(String(100))
    CodigoAsignatura = db.Column(String(20), unique=True)
    Estado = db.Column(Enum('Activa', 'Inactiva'), default='Activa')
    ID_Usuario = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'))
    ID_Programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))

class Asistencia(db.Model):
    __tablename__ = 'Asistencia'
    ID_Asistencia = db.Column(Integer, primary_key=True, autoincrement=True)
    Fecha = db.Column(Date, nullable=False)
    ID_Estudiante = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'))
    ID_programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))
    Estado = db.Column(Enum('Asistio', 'Falto'), nullable=False)
    Justificacion = db.Column(Text)

class Observacion(db.Model):
    __tablename__ = 'Observacion'
    ID_Observacion = db.Column(Integer, primary_key=True, autoincrement=True)
    Fecha = db.Column(Date, nullable=False)
    Descripcion = db.Column(Text)
    Tipo = db.Column(Enum('Academica', 'Convivencial'))
    NivelImportancia = db.Column(Enum('Bajo', 'Medio', 'Alto'))
    Recomendacion = db.Column(Text)
    Estado = db.Column(Enum('Activa', 'Inactiva'))
    ID_Programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))
    ID_Matricula = db.Column(Integer, ForeignKey('Matricula.ID_Matricula'))

class Actividad(db.Model):
    __tablename__ = 'Actividad'
    ID_Actividad = db.Column(Integer, primary_key=True, autoincrement=True)
    Titulo = db.Column(String(200), nullable=False)
    Tipo = db.Column(Enum('Taller', 'Examen', 'Participacion', 'Grupo'))
    Fecha = db.Column(Date)
    ID_Usuario = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'))
    ID_Programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))
    ID_Periodo = db.Column(Integer, ForeignKey('Periodo.ID_Periodo'))
    Estado = db.Column(Enum('Pendiente', 'Calificada', 'Cancelada'))
    Observacion = db.Column(Text)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Enum, Text, ForeignKey, DECIMAL, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import YEAR
from flask_login import UserMixin

db = SQLAlchemy()

# Definir las clases para cada tabla. El orden es crucial para evitar errores de clave foránea.
# Las tablas sin dependencias se definen primero.
class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    ID_Usuario = db.Column(Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(String(100), nullable=False)
    Apellido = db.Column(String(100), nullable=False)
    Correo = db.Column(String(150), unique=True, nullable=False)
    Contrasena = db.Column(String(255), nullable=False)
    TipoDocumento = db.Column(String(50))
    NumeroDocumento = db.Column(String(50), unique=True)
    Direccion = db.Column(String(200))
    Telefono = db.Column(String(50))
    Estado = db.Column(Enum('Activo', 'Inactivo'), default='Activo')
    Calle = db.Column(String(100))
    Ciudad = db.Column(String(100))
    Departamento = db.Column(String(100))
    Genero = db.Column(Enum('M', 'F', 'Otro'))
    Rol = db.Column(Enum('Administrador', 'Docente', 'Estudiante', 'Acudiente'), nullable=False)

    # Relaciones inversas
    matriculas = relationship('Matricula', backref='usuario', lazy=True)
    programaciones_docente = relationship('Programacion', backref='docente', lazy=True, foreign_keys='Programacion.ID_Usuario')
    asistencias = relationship('Asistencia', backref='estudiante', lazy=True)
    actividades = relationship('Actividad', backref='usuario_actividad', lazy=True)
    asignaturas = relationship('Asignatura', backref='usuario_asignatura', lazy=True)
    
    def get_id(self):
        return str(self.ID_Usuario)


class Matricula(db.Model):
    __tablename__ = 'Matricula'
    ID_Matricula = db.Column(Integer, primary_key=True, autoincrement=True)
    ID_Estudiante = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'), nullable=False)
    Correo = db.Column(String(150))
    FechaNacimiento = db.Column(Date)
    DepNacimiento = db.Column(String(100))
    TipoDocumento = db.Column(String(50))
    NumeroDocumento = db.Column(String(50))
    AnioLectivo = db.Column(YEAR)

    # Relaciones inversas
    cursos = relationship('Curso', backref='matricula', lazy=True)
    observaciones = relationship('Observacion', backref='matricula', lazy=True)

class Periodo(db.Model):
    __tablename__ = 'Periodo'
    ID_Periodo = db.Column(Integer, primary_key=True, autoincrement=True)
    NumeroPeriodo = db.Column(Integer, nullable=False)
    Anio = db.Column(YEAR, nullable=False)
    FechaInicial = db.Column(Date)
    FechaFinal = db.Column(Date)
    Porcentaje = db.Column(DECIMAL(5, 2))
    NotaFinal = db.Column(DECIMAL(5, 2))
    
    # Relación inversa
    actividades = relationship('Actividad', backref='periodo', lazy=True)

# Las tablas con dependencias circulares se crean después de que todas las demás se hayan definido.
# Se usa `forward references` con el nombre de la tabla como string.
class Programacion(db.Model):
    __tablename__ = 'Programacion'
    ID_Programacion = db.Column(Integer, primary_key=True, autoincrement=True)
    ID_Curso = db.Column(Integer, ForeignKey('Curso.ID_Curso'))
    ID_Asignatura = db.Column(Integer, ForeignKey('Asignatura.ID_Asignatura'))
    HoraInicio = db.Column(Time)
    HoraFin = db.Column(Time)
    Dia = db.Column(String(20))
    ID_Usuario = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'))

    # Relaciones inversas
    cursos_programacion = relationship('Curso', backref='programacion', lazy=True, foreign_keys='Programacion.ID_Curso')
    asignaturas_programacion = relationship('Asignatura', backref='programacion_asignatura', lazy=True, foreign_keys='Programacion.ID_Asignatura')
    asistencias = relationship('Asistencia', backref='programacion_asistencia', lazy=True)
    observaciones = relationship('Observacion', backref='programacion_observacion', lazy=True)
    actividades = relationship('Actividad', backref='programacion_actividad', lazy=True)

class Curso(db.Model):
    __tablename__ = 'Curso'
    ID_Curso = db.Column(Integer, primary_key=True, autoincrement=True)
    Grado = db.Column(String(10), nullable=False)
    Grupo = db.Column(String(10))
    Anio = db.Column(YEAR, nullable=False)
    Estado = db.Column(Enum('Activo', 'Inactivo'), default='Activo')
    DirectorGrupo = db.Column(Integer)
    NumeroEstudiantes = db.Column(Integer)
    ID_Matricula = db.Column(Integer, ForeignKey('Matricula.ID_Matricula'))
    ID_Programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))

class Asignatura(db.Model):
    __tablename__ = 'Asignatura'
    ID_Asignatura = db.Column(Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(String(100), nullable=False)
    Descripcion = db.Column(Text)
    Grado = db.Column(String(10))
    Area = db.Column(String(100))
    CodigoAsignatura = db.Column(String(20), unique=True)
    Estado = db.Column(Enum('Activa', 'Inactiva'), default='Activa')
    ID_Usuario = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'))
    ID_Programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))

class Asistencia(db.Model):
    __tablename__ = 'Asistencia'
    ID_Asistencia = db.Column(Integer, primary_key=True, autoincrement=True)
    Fecha = db.Column(Date, nullable=False)
    ID_Estudiante = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'))
    ID_programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))
    Estado = db.Column(Enum('Asistio', 'Falto'), nullable=False)
    Justificacion = db.Column(Text)

class Observacion(db.Model):
    __tablename__ = 'Observacion'
    ID_Observacion = db.Column(Integer, primary_key=True, autoincrement=True)
    Fecha = db.Column(Date, nullable=False)
    Descripcion = db.Column(Text)
    Tipo = db.Column(Enum('Academica', 'Convivencial'))
    NivelImportancia = db.Column(Enum('Bajo', 'Medio', 'Alto'))
    Recomendacion = db.Column(Text)
    Estado = db.Column(Enum('Activa', 'Inactiva'))
    ID_Programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))
    ID_Matricula = db.Column(Integer, ForeignKey('Matricula.ID_Matricula'))

class Actividad(db.Model):
    __tablename__ = 'Actividad'
    ID_Actividad = db.Column(Integer, primary_key=True, autoincrement=True)
    Titulo = db.Column(String(200), nullable=False)
    Tipo = db.Column(Enum('Taller', 'Examen', 'Participacion', 'Grupo'))
    Fecha = db.Column(Date)
    ID_Usuario = db.Column(Integer, ForeignKey('Usuario.ID_Usuario'))
    ID_Programacion = db.Column(Integer, ForeignKey('Programacion.ID_Programacion'))
    ID_Periodo = db.Column(Integer, ForeignKey('Periodo.ID_Periodo'))
    Estado = db.Column(Enum('Pendiente', 'Calificada', 'Cancelada'))
    Observacion = db.Column(Text)
