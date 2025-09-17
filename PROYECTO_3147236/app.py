import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify  # <-- añadí send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pymysql

# --- NUEVO ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
# --- FIN NUEVO ---

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
    return render_template('Paginainicio.html')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)

@app.route('/notas')
def notas():
    return render_template('Notas.html')


@app.route('/observador')
def observador():
    return render_template('Observador.html')

@app.route('/profesores')
@login_required
def profesores():
    docentes = Usuario.query.filter_by(Rol='Docente').all()
    return render_template('Profesores.html', docentes=docentes)

@app.route('/agregar_docente', methods=['POST'])
@login_required
def agregar_docente():
    try:
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        correo = request.form['Correo']
        numero_doc = request.form['NumeroDocumento']
        telefono = request.form['Telefono']
        tipo_doc = "C.C."
        profesion = request.form['Profesion']
        ciclo = request.form['Ciclo']

        # Contraseña temporal
        hashed_password = generate_password_hash("123456")

        nuevo_docente = Usuario(
            Nombre=nombre,
            Apellido=apellido,
            Correo=correo,
            Contrasena=hashed_password,
            TipoDocumento=tipo_doc,
            NumeroDocumento=numero_doc,
            Telefono=telefono,
            Rol='Docente',
            Estado='Activo',
            Direccion="",
            Genero="Otro"
        )
        db.session.add(nuevo_docente)
        db.session.commit()
        flash("Docente agregado correctamente", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al agregar docente: {str(e)}", "danger")

    return redirect(url_for('profesores'))


# Actualizar Docente
@app.route('/actualizar_docente/<int:id>', methods=['POST'])
def actualizar_docente(id):
    docente = Usuario.query.get_or_404(id)  # Buscar por ID

    docente.Nombre = request.form['Nombre']
    docente.Apellido = request.form['Apellido']
    docente.TipoDocumento = request.form['TipoDocumento']
    docente.NumeroDocumento = request.form['NumeroDocumento']
    docente.Correo = request.form['Correo']
    docente.Telefono = request.form['Telefono']
    docente.Direccion = request.form['Profesion']
    docente.Calle = request.form['Ciclo']

    try:
        db.session.commit()
        flash("Docente actualizado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {e}", "danger")

    return redirect(url_for('profesores'))


# Eliminar Docente
@app.route('/eliminar_docente/<int:id>', methods=['POST'])
@login_required
def eliminar_docente(id):
    docente = Usuario.query.get_or_404(id)
    try:
        db.session.delete(docente)
        db.session.commit()
        flash("Docente eliminado correctamente", "danger")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al eliminar docente: {str(e)}", "danger")

    return redirect(url_for('profesores'))


# ---------------- ESTUDIANTES ----------------

@app.route('/estudiantes')
@login_required
def estudiantes():
    estudiantes = Usuario.query.filter_by(Rol='Estudiante').all()
    return render_template('Estudiantes.html', estudiantes=estudiantes)


@app.route('/agregar_estudiante', methods=['POST'])
@login_required
def agregar_estudiante():
    try:
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        correo = request.form['Correo']
        numero_doc = request.form['NumeroDocumento']
        telefono = request.form['Telefono']
        tipo_doc = request.form['TipoDocumento']
        direccion = request.form['Direccion']
        curso = request.form['Curso']

        hashed_password = generate_password_hash("123456")

        nuevo_estudiante = Usuario(
            Nombre=nombre,
            Apellido=apellido,
            Correo=correo,
            Contrasena=hashed_password,
            TipoDocumento=tipo_doc,
            NumeroDocumento=numero_doc,
            Telefono=telefono,
            Rol='Estudiante',
            Estado='Activo',
            Direccion=direccion,
            Calle=curso,
            Genero="Otro"
        )
        db.session.add(nuevo_estudiante)
        db.session.commit()
        flash("Estudiante agregado correctamente", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al agregar estudiante: {str(e)}", "danger")

    return redirect(url_for('estudiantes'))


@app.route('/actualizar_estudiante/<int:id>', methods=['POST'])
@login_required
def actualizar_estudiante(id):
    estudiante = Usuario.query.get_or_404(id)

    estudiante.Nombre = request.form['Nombre']
    estudiante.Apellido = request.form['Apellido']
    estudiante.TipoDocumento = request.form['TipoDocumento']
    estudiante.NumeroDocumento = request.form['NumeroDocumento']
    estudiante.Correo = request.form['Correo']
    estudiante.Telefono = request.form['Telefono']
    estudiante.Direccion = request.form['Direccion']
    estudiante.Calle = request.form['Curso']

    try:
        db.session.commit()
        flash("Estudiante actualizado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {e}", "danger")

    return redirect(url_for('estudiantes'))


@app.route('/eliminar_estudiante/<int:id>', methods=['POST'])
@login_required
def eliminar_estudiante(id):
    estudiante = Usuario.query.get_or_404(id)
    try:
        db.session.delete(estudiante)
        db.session.commit()
        flash("Estudiante eliminado correctamente", "danger")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al eliminar estudiante: {str(e)}", "danger")

    return redirect(url_for('estudiantes'))


# ---------------- ACUDIENTES ----------------

@app.route('/acudientes')
@login_required
def acudientes():
    acudientes = Usuario.query.filter_by(Rol='Acudiente').all()
    return render_template('Acudientes.html', acudientes=acudientes)


@app.route('/agregar_acudiente', methods=['POST'])
@login_required
def agregar_acudiente():
    try:
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        correo = request.form['Correo']
        numero_doc = request.form['NumeroDocumento']
        telefono = request.form['Telefono']
        tipo_doc = request.form['TipoDocumento']
        direccion = request.form['Direccion']

        hashed_password = generate_password_hash("123456")

        nuevo_acudiente = Usuario(
            Nombre=nombre,
            Apellido=apellido,
            Correo=correo,
            Contrasena=hashed_password,
            TipoDocumento=tipo_doc,
            NumeroDocumento=numero_doc,
            Telefono=telefono,
            Direccion=direccion,
            Rol='Acudiente',
            Estado='Activo',
            Genero="Otro"
        )
        db.session.add(nuevo_acudiente)
        db.session.commit()
        flash("Acudiente agregado correctamente", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al agregar acudiente: {str(e)}", "danger")

    return redirect(url_for('acudientes'))


@app.route('/actualizar_acudiente/<int:id>', methods=['POST'])
@login_required
def actualizar_acudiente(id):
    acudiente = Usuario.query.get_or_404(id)

    acudiente.Nombre = request.form['Nombre']
    acudiente.Apellido = request.form['Apellido']
    acudiente.TipoDocumento = request.form['TipoDocumento']
    acudiente.NumeroDocumento = request.form['NumeroDocumento']
    acudiente.Correo = request.form['Correo']
    acudiente.Telefono = request.form['Telefono']
    acudiente.Direccion = request.form['Direccion']

    try:
        db.session.commit()
        flash("Acudiente actualizado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {e}", "danger")

    return redirect(url_for('acudientes'))


@app.route('/eliminar_acudiente/<int:id>', methods=['POST'])
@login_required
def eliminar_acudiente(id):
    acudiente = Usuario.query.get_or_404(id)
    try:
        db.session.delete(acudiente)
        db.session.commit()
        flash("Acudiente eliminado correctamente", "danger")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al eliminar acudiente: {str(e)}", "danger")

    return redirect(url_for('acudientes'))


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

@app.route('/reunion')
def reunion():
    return render_template('Reunion.html')


@app.route('/noticias')
def noticias():
    return render_template('Noticias.html')

@app.route('/circulares')
def circulares():
    return render_template('Circulares.html')

@app.route('/noticias_vistas')
def noticias_vistas():
    return render_template('NoticiasVistas.html')

@app.route('/usuarios')
def usuarios():
    return render_template('Usuarios.html')

@app.route('/asignaturas')
def asignaturas():
    return render_template('Asignaturas.html')

@app.route('/horarios')
def horarios():
    return render_template('Horarios.html')

@app.route('/registro_notas/<int:curso_id>')
def registro_notas(curso_id):
    return render_template('RegistroNotas.html', curso_id=curso_id)

#Conexión de los cursos
@app.route('/notas/<int:curso_id>')
def notas_curso(curso_id):
    return render_template("notas_curso.html", curso_id=curso_id)


@app.route('/notasr')
def notasr():
    return render_template('NotasR.html')

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

        tipo_documento = request.form.get('TipoDocumento', 'CC')
        estado = request.form.get('Estado', 'Activo')
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

#sub-inicio
@app.route('/materialapoyo2')
def materialapoyo2():
    return render_template('MaterialApoyo2.html')

@app.route('/registrotutorias2')
def registrotutorias2():
    return render_template('RegistroTutorías2.html')


# ========================
# --- NUEVO: RESUMEN SEMANAL ---
# ========================
def generar_pdf(actividades, problemas, filename="resumen.pdf"):
    """Genera un PDF con actividades y problemas"""
    filepath = os.path.join(os.getcwd(), filename)
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, height - 50, "📄 Resumen Semanal")

    c.setFont("Helvetica", 12)
    y = height - 100

    c.drawString(50, y, "✅ Actividades realizadas:")
    y -= 20
    for act in actividades:
        c.drawString(70, y, f"- {act}")
        y -= 15

    y -= 20
    c.drawString(50, y, "⚠️ Problemas registrados:")
    y -= 20
    for prob in problemas:
        c.drawString(70, y, f"- {prob}")
        y -= 15

    c.save()
    return filepath


def enviar_resumen_pdf(destinatarios, pdf_path="resumen.pdf"):
    """Envía el PDF por correo usando Gmail"""
    remitente = "tucorreo@gmail.com"
    password = "tu_contraseña_de_aplicacion"

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = "Resumen semanal de actividades"

    msg.attach(MIMEText("Adjunto encontrarás el resumen semanal en PDF.", "plain"))

    with open(pdf_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=pdf_path)
        msg.attach(attach)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, destinatarios, msg.as_string())
        server.quit()
        print("Resumen enviado correctamente.")
    except Exception as e:
        print("Error al enviar correo:", e)


@app.route('/generar', methods=['POST'])   # 👈 ahora coincide con tu resumen.js
def generar_resumen():
    """Genera un PDF y lo devuelve como descarga"""
    data = request.get_json()
    actividades = data.get("actividades", [])
    problemas = data.get("problemas", [])

    filename = generar_pdf(actividades, problemas)
    return send_file(filename, as_attachment=True)


@app.route('/enviar_resumen', methods=['POST'])
def enviar_resumen():
    """Genera un PDF y lo envía por correo"""
    data = request.get_json()
    actividades = data.get("actividades", [])
    problemas = data.get("problemas", [])
    destinatarios = data.get("destinatarios", ["docente@colegio.com"])

    filename = generar_pdf(actividades, problemas)
    enviar_resumen_pdf(destinatarios, filename)

    return jsonify({"message": "Resumen enviado por correo."})


def tarea_programada():
    actividades = ["Clases realizadas", "Reuniones", "Asistencia"]
    problemas = ["Error en registro de notas", "Falla en servidor"]

    filename = generar_pdf(actividades, problemas)
    enviar_resumen_pdf(["docente@colegio.com", "gisellleal491@gmail.com"], filename)


scheduler = BackgroundScheduler()
scheduler.add_job(tarea_programada, 'cron', day_of_week='tue', hour=19, minute=10)


if __name__ == "__main__":
    app.run(debug=True)
