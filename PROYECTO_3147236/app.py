from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "clave-secreta"

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
