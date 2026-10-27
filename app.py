from flask import Flask

# Criar a instância da aplicação web
app = Flask(__name__)

# Definir uma rota de teste simples
@app.route("/")
def home():
    return "Olá, minhas divasss"

# Rodar o servidor local
if __name__ == "__main__":
    app.run(debug=True)