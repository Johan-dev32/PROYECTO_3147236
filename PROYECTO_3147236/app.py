import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pymysql

# Importa el objeto 'db' y los modelos desde tu archivo de modelos
from database.models import db, Usuario

# Configuración de la aplicación
app = Flask(__name__)

# Configuración de la base de datos
DB_URL = 'mysql+pymysql://root:@127.0.0.1:3306/edunotas'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_super_secreta'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}

# Inicializa la instancia de SQLAlchemy con la aplicación
db.init_app(app)

# Inicialización de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Esta función es requerida por Flask-Login para cargar un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Crea la base de datos y las tablas si no existen
with app.app_context():
    engine = create_engine(DB_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Base de datos 'edunotas' creada exitosamente.")
    db.create_all()
    print("Tablas de la base de datos creadas exitosamente.")

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def index():
   return render_template("Login.html")


@app.route('/paginainicio')
def paginainicio():
    return render_template('PaginaInicio.html')

@app.route('/notas')
def notas():
    return render_template('Notas.html')



@app.route('/observador')
def observador():
    return render_template('Observador.html')

@app.route('/profesores')
def profesores():
    return render_template('Profesores.html')

@app.route('/manual')
def manual():
    return render_template('ManualUsuario.html')

@app.route('/resumensemanal')
def resumensemanal():
    return render_template('ResumenSemanal.html')

@app.route('/registrotutorias')
def registrotutorias():
    return render_template('RegistroTutorías.html')

@app.route('/comunicacion')
def comunicacion():
    return render_template('Comunicación.html')

@app.route('/materialapoyo')
def materialapoyo():
    return render_template('MaterialApoyo.html')




@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('Nombre')
        apellido = request.form.get('Apellido')
        correo = request.form.get('Correo')
        contrasena = request.form.get('Contrasena')
        numero_documento = request.form.get('NumeroDocumento')
        telefono = request.form.get('Telefono')
        direccion = request.form.get('Direccion')
        rol = request.form.get('Rol')

        # Se añaden valores por defecto para los campos faltantes en el formulario
        tipo_documento = request.form.get('TipoDocumento', 'CC')  # Valor por defecto 'CC'
        estado = request.form.get('Estado', 'Activo')  # Valor por defecto 'Activo'
        genero = request.form.get('Genero', '')
        
        if not all([nombre, apellido, correo, contrasena, numero_documento, telefono, direccion, rol]):
            flash('Por favor, completa todos los campos requeridos.')
            return render_template('Registro.html')

        try:
            existing_user = Usuario.query.filter_by(Correo=correo).first()
            if existing_user:
                flash('El correo electrónico ya está registrado. Por favor, usa otro.')
                return render_template('Registro.html')

            hashed_password = generate_password_hash(contrasena)
            
            new_user = Usuario(
                Nombre=nombre,
                Apellido=apellido,
                Correo=correo,
                Contrasena=hashed_password,
                TipoDocumento=tipo_documento,
                NumeroDocumento=numero_documento,
                Telefono=telefono,
                Direccion=direccion,
                Rol=rol,
                Estado=estado,
                Genero=genero
            )
            
            print(f'Intentando agregar usuario: {new_user.Correo}')
            db.session.add(new_user)
            db.session.commit()

            flash('Cuenta creada exitosamente! Por favor, inicia sesión.')
            return redirect(url_for('login'))
        
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Ocurrió un error al intentar registrar el usuario: {str(e)}')
            return render_template('Registro.html')

    return render_template('Registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Por favor, ingresa tu correo y contraseña.')
            return render_template('login.html')

        user = Usuario.query.filter_by(Correo=email).first()

        if user and check_password_hash(user.Contrasena, password):
            login_user(user)
            flash('Has iniciado sesión con éxito!')
            return redirect(url_for('paginainicio'))
        else:
            flash('Credenciales inválidas. Por favor, revisa tu correo y contraseña.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('Profesores.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('index'))

#sub-inicio osea que ya no son del inicio si no de otras funciones


if __name__ == '__main__':
    app.run(debug=True)
