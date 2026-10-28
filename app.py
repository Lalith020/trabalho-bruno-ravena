from flask import Flask
from routes.operacao_routes import operacao_bp

# Criar a instância da aplicação web
app = Flask(__name__)
app.secret_key = 'iconic_diva' # Necessário para as mensagens flash funcionarem

# Registar o Blueprint com as rotas completas do nosso MVC
app.register_blueprint(operacao_bp)

# Rodar o servidor local
if __name__ == "__main__":
    app.run(debug=True)