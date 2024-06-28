from flask import Flask, request, render_template, redirect,  session
from cs50 import SQL
from datetime import datetime
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, admin_required
from flask_socketio import SocketIO, send

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Conexion a la base de datos
db = SQL("sqlite:///formulario.db")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("apology.html")

        elif not request.form.get("password"):
            return render_template("apology.html")

        rows = db.execute(
            "SELECT * FROM personas WHERE nombre = ?", request.form.get(
                "username")
            )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
            ):
            return render_template("apology.html")

        session["user_id"] = rows[0]["id"]
        session["role"] = rows[0]["role"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/cerrarSesion")
def cerrarSesion():
    session.clear()
    return redirect("/")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("username")
        contraseña = request.form.get("password")
        correo = request.form.get("correo")
        hashpass = generate_password_hash(contraseña)
        if db.execute(
            "SELECT nombre FROM personas WHERE nombre= ?", nombre
        ):
            return render_template("apology.html")
        if db.execute(
          "SELECT correo FROM personas WHERE correo=?", correo
        ):
            return render_template("apology.html")
        if not nombre:
            return render_template("apology.html")
        if not contraseña:
            return render_template("apology.html")
        if not correo:
            return render_template("apology.html")
        elif request.form.get("password(again)") != contraseña:
            return render_template("apology.html")

        sesion = db.execute(
            "INSERT INTO personas (nombre, hash, correo, role) VALUES (?,?,?,?)", nombre, hashpass, correo, "user"
        )
        session["user_id"] = sesion
        return redirect("/")

    else:
        return render_template("registro.html")


@app.route("/forgot", methods=["GET", "POST"])
def new_pass():
    if request.method == "POST":
        usuario = request.form.get("username")
        correo = request.form.get("correo")
        pass_new = request.form.get("new_pass")
        hashpass = generate_password_hash(pass_new)

        if not request.form.get("new_pass"):
            return render_template("apology.html")

        if db.execute("SELECT nombre FROM personas WHERE nombre=?", usuario) or db.execute("SELECT correo FROM personas WHERE correo=?", correo):
            db.execute("UPDATE personas SET hash=? WHERE nombre = ?", hashpass, usuario)
            return redirect("/")
        else:
            return render_template("apology.html")
    else:
        return render_template("forgot.html")


@app.route("/formulario", methods=["GET", "POST"])
@login_required
def formulario():
    submission_time = None
    if request.method == "POST":
            # Entradas del formulario
        submission_time = datetime.now().strftime('%Y-%m-%d')
        restaurante = request.form.get("restaurante")
        if not restaurante:
            return render_template("apology.html")
        nombre_mesero = request.form.get("nombre_mesero")
        if not nombre_mesero:
            return render_template("apology.html")
        calidadComida = request.form.get("calidadcomida")
        calidad_servicio = request.form.get("calidadServicio")
        ambiente = request.form.get("calidadinstalaciones")
        limpieza = request.form.get("limpieza")
        promo = request.form.get("promo")
        amabilidad = request.form.get("amabilidad")
        comentario = request.form.get("comentario")
            # Selecciona id restaurante
        restaurante_id = db.execute(
            "SELECT id FROM restaurantes WHERE restaurante = ?", restaurante
        )
            # Selecciona id mesero
        mesero_id = db.execute(
            "SELECT id FROM meseros WHERE nombreMesero = ?", nombre_mesero
        )
        if db.execute(
            "SELECT id_cliente FROM calidadServicio WHERE id_cliente = ?", session["user_id"]
        ):
            db.execute(
                "UPDATE calidadServicio SET calidad_servicio = ?, amabilidad = ?, promo = ?, id_mesero = ?, comentario = ?, fecha = ? WHERE id_cliente = ?",
                calidad_servicio, amabilidad, promo, mesero_id[0]["id"], comentario, submission_time, session["user_id"]
            )
            db.execute(
                "UPDATE calidadInstalaciones SET calidad_comida = ?, ambiente = ?,  limpiezaBaños = ?, id_restaurante = ? WHERE id_cliente = ?",
                calidadComida, ambiente, limpieza, restaurante_id[0]["id"], session["user_id"]
            )
        else:
            db.execute(
                "INSERT INTO calidadServicio (calidad_servicio,amabilidad,promo,id_mesero,id_cliente, comentario, fecha) VALUES(?,?,?,?,?,?,?)",
                calidad_servicio, amabilidad, promo, mesero_id[0]["id"], session["user_id"], comentario, submission_time
            )
            db.execute(
                "INSERT INTO calidadInstalaciones(calidad_comida,ambiente,limpiezaBaños,id_cliente,id_restaurante) VALUES(?,?,?,?,?)",
                calidadComida, ambiente, limpieza, session["user_id"], restaurante_id[0]["id"]
            )
        return redirect("/")
    else:
        restaurantes = db.execute(
            "SELECT restaurante FROM restaurantes"
        )
        meseros = db.execute(
            "SELECT nombreMesero FROM meseros"
        )
        return render_template("formulario.html", restaurantes=restaurantes, meseros= meseros)


@app.route("/eventos", methods=["GET", "POST"])
@login_required
def eventos():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("eventos.html")


@app.route("/admin")
@login_required
@admin_required
def admin():
    # personas que enviaron formulario
    pf = db.execute(
        "SELECT id FROM personas WHERE id IN (SELECT id_cliente FROM calidadServicio) AND id IN (SELECT id_cliente FROM calidadInstalaciones)"
    )
    cu = 0
    nombre = []
    comentario = []
    restaurante = []
    mesero = []
    calidadInstalaciones = []
    calidadComida = []
    limpiezaBaños = []
    ambienteInstalaciones = []
    calidadServicio = []
    calidad_servicio = []
    amabilidad = []
    promo = []
    fecha = []

    for i in range(len(pf)):
        nombre.append(
            db.execute(
            "SELECT nombre FROM personas WHERE id = ?", pf[i]["id"]
        ))

        comentario.append(
            db.execute(
            "SELECT comentario FROM calidadServicio WHERE id_cliente = ?", pf[i]["id"]
        ))

        restaurante.append(
            db.execute(
                 "SELECT restaurante FROM restaurantes WHERE id IN (SELECT id_restaurante FROM calidadInstalaciones WHERE id_cliente = ?)", pf[i]["id"]
                 ))
        calidadInstalaciones.append(
            db.execute(
                "SELECT * FROM calidadInstalaciones WHERE id_cliente= ?", pf[i]["id"]
            ))
        limpiezaBaños.append(calidadInstalaciones[i][0]["limpiezaBaños"])
        ambienteInstalaciones.append(calidadInstalaciones[i][0]["ambiente"])
        calidadComida.append(calidadInstalaciones[i][0]["calidad_comida"])
        mesero.append(
            db.execute(
                 "SELECT nombreMesero FROM meseros WHERE id IN (SELECT id_mesero FROM calidadServicio WHERE id_cliente = ?)", pf[i]["id"]
                 ))
        calidadServicio.append(
            db.execute(
                "SELECT * FROM calidadServicio WHERE id_cliente= ?", pf[i]["id"]
            ))
        calidad_servicio.append(calidadServicio[i][0]["calidad_servicio"])
        amabilidad.append(calidadServicio[i][0]["amabilidad"])
        promo.append(calidadServicio[i][0]["promo"])
        fecha.append(
            db.execute(
                "SELECT fecha FROM calidadServicio WHERE id_cliente= ?", pf[i]["id"]
            ))

        # cantidad usuarios
        cu = cu + 1
    return render_template(
        "dbAdmin.html", nombre=nombre, comentario= comentario, cantidadUsuarios= cu, restaurante= restaurante, mesero= mesero,
        limpiezaBaños=limpiezaBaños, calidadServicio= calidad_servicio, ambienteInstalaciones= ambienteInstalaciones, calidadComida= calidadComida,
        amabilidad=amabilidad, promo=promo, fecha= fecha
    )
