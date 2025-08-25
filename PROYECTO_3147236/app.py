from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave-secreta"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pruebaedu"
)

@app.route("/")
def index():
    return render_template("Login.html")

@app.route("/registro")
def registro():
    return render_template("Registro.html")


@app.route("/login", methods=["POST"])
def login():
    correo = request.form["correo"]
    contrasena = request.form["contrasena"]

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE correo=%s AND contrasena=%s", (correo, contrasena))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario:
        session["usuario"] = usuario["Correo"]
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

if __name__ == "__main__":
    app.run(debug=True)