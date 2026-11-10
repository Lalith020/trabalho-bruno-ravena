from flask import Flask
from routes.operacao_routes import registrar_rotas

# Cria o app Flask: pense nele como a base dos Vingadores, onde tudo se conecta.
app = Flask(__name__)
app.secret_key = 'iconic_diva'  # Assina a sessão para as mensagens flash, como um selo de autenticidade.

# Liga os endereços do site às funções que atendem cada página.
registrar_rotas(app)

# Inicia o servidor apenas quando este arquivo é executado diretamente.
if __name__ == "__main__":
    app.run(debug=True)  # Debug ajuda a encontrar erros durante o desenvolvimento.