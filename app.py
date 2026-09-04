from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-temporaria")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

USUARIO = os.environ.get("ADMIN_USER", "admin")
SENHA = os.environ.get("ADMIN_PASSWORD", "troque-esta-senha")

ARQUIVO_REGISTROS = "registros.csv"


class Usuario(UserMixin):
    id = "admin"


@login_manager.user_loader
def carregar_usuario(user_id):
    if user_id == "admin":
        return Usuario()
    return None


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/registrar", methods=["POST"])
def registrar():
    nome = request.form.get("nome", "").strip()
    latitude = request.form.get("latitude", "").strip()
    longitude = request.form.get("longitude", "").strip()

    if not nome or not latitude or not longitude:
        return "Cadastro incompleto.", 400

    novo_arquivo = not os.path.exists(ARQUIVO_REGISTROS)

    with open(ARQUIVO_REGISTROS, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        if novo_arquivo:
            escritor.writerow(["data", "nome", "latitude", "longitude"])

        escritor.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            nome,
            latitude,
            longitude
        ])

    return "Cadastro realizado com sucesso!"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == USUARIO and senha == SENHA:
            login_user(Usuario())
            return redirect(url_for("registros"))

        return "Usuário ou senha incorretos.", 401

    return '''
    <h1>Acesso aos registros</h1>
    <form method="post">
        <input name="usuario" placeholder="Usuário" required><br><br>
        <input name="senha" type="password" placeholder="Senha" required><br><br>
        <button type="submit">Entrar</button>
    </form>
    '''


@app.route("/registros")
@login_required
def registros():
    if not os.path.exists(ARQUIVO_REGISTROS):
        dados = []
    else:
        with open(ARQUIVO_REGISTROS, newline="", encoding="utf-8") as arquivo:
            dados = list(csv.DictReader(arquivo))

    return render_template("registros.html", registros=dados)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
