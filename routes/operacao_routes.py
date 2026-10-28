# Importa o Blueprint para organizar as rotas, além de funções para renderizar páginas, pegar dados de formulários e redirecionar
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Importa o controller para podermos chamar as regras de negócio e salvar/listar as operações
from controllers.operacao_controller import OperacaoController

# Cria o Blueprint para as rotas de operação
operacao_bp = Blueprint('operacao', __name__)

# Instancia o controller para usarmos nas rotas abaixo
controller = OperacaoController()

# Rota principal: busca todas as operações cadastradas e exibe na página de listagem
@operacao_bp.route('/')
def listar():
    operacoes = controller.listar_operacoes()
    return render_template('listar.html', operacoes=operacoes)

# Rota para cadastrar nova operação: lida tanto com a exibição do formulário (GET) quanto com o envio dos dados (POST)
@operacao_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        # Pega os dados enviados pelo formulário HTML
        data = request.form.get('data')
        ativo = request.form.get('ativo')
        quantidade = request.form.get('quantidade')
        valor_unitario = request.form.get('valor_unitario')
        tipo_operacao = request.form.get('tipo_operacao')
        
        # Envia os dados para o controller validar e tentar salvar
        sucesso, resultado = controller.cadastrar_operacao(data, ativo, quantidade, valor_unitario, tipo_operacao)
        
        if sucesso:
            # Se deu certo, mostra mensagem de sucesso e redireciona pra lista
            flash(resultado, 'success')
            return redirect(url_for('operacao.listar'))
        else:
            # Se deu erro, mostra os erros de validação na tela para o usuário corrigir
            for erro in resultado:
                flash(erro, 'danger')
                
    # Se for GET, apenas renderiza a página do formulário de cadastro
    return render_template('cadastrar.html')