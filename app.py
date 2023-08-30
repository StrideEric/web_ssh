from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)


@app.route("/")
def index():
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
    if command == "lscpu":
        full_command = f"lscpu {plscpu}"
    if "meminfo" in command:
        full_command = command
    if command == "vmstat":
        full_command = command
    if command == "stress":
        full_command = "stress --vm 1 --vm-bytes 1G"
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
    #return render_template("index.html", output=output)
    return output

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
