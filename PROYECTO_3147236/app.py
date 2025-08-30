from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from database.models import db, Usuario


# Configuración de la base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/edunotas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "clave-secreta"

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

if __name__ == "__main__":
    app.run(debug=True)
