from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import paramiko

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db = SQLAlchemy(app)


class Contador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contador = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str(self.contador) if self.contador is not None else None


@app.route("/create_tables", methods=["GET"])
def create_tables():
    with app.app_context():
        db.create_all()
        __init = Contador(contador=0)
        db.session.add(__init)
        db.session.commit()
        return "Database tables created"


@app.route("/")
def index():
    contador = Contador.query.all()
    for c in contador:
        print(str(c))

    return render_template("index.html")


@app.route("/execute_ssh_command", methods=["POST"])
def execute_ssh_command():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = "192.168.66.128"
    username = "mdfk"
    password = "asdpoasd"
    command = request.form.get("command")
    p = request.form.get("p")
    c = request.form.get("c")
    m = request.form.get("m")
    parameters = request.form.get("parameters")
    pfree = request.form.get("pfree")
    plscpu = request.form.get("plscpu")

    full_command = ""

    if command == "free":
        full_command = f"free {pfree}"  # Combina el comando con los parámetros
    elif command == "lscpu":
        full_command = f"lscpu {plscpu}"
    elif "meminfo" in command:
        full_command = command
    elif command == "vmstat":
        full_command = command
    elif command == "stress":
        contadores = Contador.query.all()
        if contadores:
            primero = contadores[0]
            if primero.contador >= 5:
                return "Ya se enviaron muchos comandos stress :<"
            primero.contador = primero.contador + 1
            db.session.commit()

        full_command = "stress --vm 1 --vm-bytes 500MB"
    else:
        return "Comando inválido"
    full_command = full_command.strip()

    # stress --vm 4 --vm-bytes 2G

    try:
        ssh.connect(host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(full_command)
        output = stdout.read().decode("utf-8")
    except Exception as e:
        output = str(e)
    finally:
        ssh.close()
    # return render_template("index.html", output=output)
    return output


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
