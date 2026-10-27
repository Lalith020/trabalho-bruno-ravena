from flask import Flask
from routes.operacao_routes import operacao_bp

app = Flask(__name__)
app.secret_key = "ravena_diva"

app.register_blueprint(operacao_bp)

if __name__ == '__main__':
    app.run(debug=True)