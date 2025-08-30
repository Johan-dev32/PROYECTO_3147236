from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from database.models import db, Usuario


# Configuración de la base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/EduNotas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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
        Contrasena = request.form.get('Contrasena')
        NumeroDocumento = request.form.get('NumeroDocumento')
        Telefono = request.form.get('Telefono')
        Direccion = request.form.get('Direccion')
        Rol = request.form.get('Rol')

        if not all([Nombre, Apellido, Correo, Contrasena, NumeroDocumento, Telefono, Rol,Direccion]):
            flash('Por favor, completa todos los campos requeridos.', 'danger')
            return render_template('registro.html')

        try:
            print(f"Usuario registrado: {Nombre} {Apellido}, Rol: {Rol}")
            
            flash('✅ Los datos se han guardado exitosamente.', 'success')
            
            return redirect(url_for('registro'))
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            flash('Ocurrió un error al guardar los datos. Inténtalo de nuevo.', 'danger')

    return render_template('Registro.html')

       
@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
