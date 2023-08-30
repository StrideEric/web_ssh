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
    parameters = request.form.get("parameters")

    full_command = f"{command} {parameters}"  # Combina el comando con los parámetros

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
    app.run(host="192.168.137.1", port=5000)
