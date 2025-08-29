from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from database.models import db, Usuario, Cliente


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
@app.route("/")
def index():
    return render_template("Login.html")

@app.route("/registro", methods=["GET", 'POST'])
def registro():
    return render_template("Registro.html")

@app.route("/login", methods=["POST"])
def login():
    correo = request.form["correo"]
    contrasena = request.form["contrasena"]

    # Simulación de usuario válido (temporal)
    if correo == "admin@ejemplo.com" and contrasena == "1234":
        session["usuario"] = correo
        return redirect(url_for("inicio"))
    else:
        flash("Correo o contraseña incorrectos", "danger")
        return redirect(url_for("index"))

@app.route("/inicio")
def inicio():
    if "usuario" in session:
        return render_template("Paginainicio.html", usuario=session["usuario"])
    else:
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))

@app.route("/notas")
def notas():
    if "usuario" in session:
        return render_template("Notas.html")
    else:
        return redirect(url_for("index"))

@app.route("/observador")
def observador():
    if "usuario" in session:
        return render_template("Observador.html")
    else:
        return redirect(url_for("index"))

@app.route("/profesores")
def profesores():
    if "usuario" in session:
        return render_template("Profesores.html")
    else:
        return redirect(url_for("index"))

@app.route("/manual")
def manual():
    if "usuario" in session:
        return render_template("ManualUsuario.html")
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
