from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def inicio():
    print("IP:", request.remote_addr)
    print("Navegador:", request.headers.get("User-Agent"))
    print("Idioma:", request.headers.get("Accept-Language"))

    return "Dados registrados no Termux!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

