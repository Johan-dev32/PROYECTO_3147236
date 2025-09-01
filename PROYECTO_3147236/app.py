from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from database.models import db, Usuario
from sqlalchemy.exc import SQLAlchemyError



# Configuración de la base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/edunotas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta'


# Inicialización de la base de datos y Flask-Login
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Esta función es requerida por Flask-Login para cargar un usuario
@login_manager.user_loader
def load_user(user_id):
    #La función debe devolver una instancia de la clase que hereda de UserMixin
    return Usuario.query.get(int(user_id))

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('Paginainicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        Nombre = request.form.get('Nombre')
        Apellido = request.form.get('Apellido')
        Correo = request.form.get('Correo')
        Contrasena = request.form.get('Contraseña')
        TipoDocumento = request.form.get('tipoDocumento')
        NumeroDocumento = request.form.get('numeroDocumento')

        if not Nombre or not Apellido or not Correo or not Contrasena or not TipoDocumento or not NumeroDocumento:
            flash('Por favor, completa todos los campos requeridos.')
            return render_template('Registro.html')

        try:
            # CORREGIDO: Uso de db.session.query para consultar la base de datos
            existing_user = db.session.query(Usuario).filter_by(Correo=Correo).first()
            if existing_user:
                flash('El correo electrónico ya está registrado. Por favor, usa otro.')
                return render_template('Registro.html')

            new_user = Usuario(Nombre=Nombre, Apellido=Apellido, Correo=Correo, Contraseña=Contrasena, TipoDocumento=TipoDocumento, NumeroDocumento=NumeroDocumento)

            db.session.add(new_user)
            db.session.commit()

            flash('Cuenta creada exitosamente! Por favor, inicia sesión.')
            return redirect(url_for('login'))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Ocurrió un error al intentar registrar el usuario: {str(e)}')
            return render_template('Registro.html')

    return render_template('Registro.html')

       
@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/paginainicio')
def paginainicio():
    return render_template('Paginainicio.html')

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

@app.route('/resumen')
def resumen():
    return render_template('ResumenSemanal.html')

if __name__ == "__main__":
    app.run(debug=True)
