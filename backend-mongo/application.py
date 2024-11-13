import os

from flask import Flask
from flask_bootstrap import Bootstrap
# Importando a função init_app de routes.py
from routes import init_app

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave aleatória para segurança

# Inicializando o Bootstrap no app
Bootstrap(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Inicializando as rotas da API e das views
init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
