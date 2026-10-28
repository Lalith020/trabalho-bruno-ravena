# Importa o Blueprint para organizar as rotas e funções essenciais do Flask
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Importa o controller para chamar a lógica de negócio e BD
from controllers.operacao_controller import OperacaoController

# Cria o Blueprint para as rotas de operação
operacao_bp = Blueprint('operacao', __name__)

# Instancia o controller
controller = OperacaoController()

# Rota principal (Listagem e Pesquisas)
@operacao_bp.route('/')
def listar():
    # Verifica se o usuário está a fazer alguma pesquisa na barra de busca
    tipo_busca = request.args.get('tipo_busca')
    termo = request.args.get('termo')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    if tipo_busca == 'id' and termo:
        op = controller.buscar_por_id(termo)
        operacoes = [op] if op else []
    elif tipo_busca == 'ativo' and termo:
        operacoes = controller.pesquisar_por_ativo(termo)
    elif tipo_busca == 'datas' and data_inicio and data_fim:
        operacoes = controller.pesquisar_por_datas(data_inicio, data_fim)
    else:
        operacoes = controller.listar_operacoes()

    return render_template('listar.html', operacoes=operacoes)

# Rota para cadastrar nova operação
@operacao_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        data = request.form.get('data')
        ativo = request.form.get('ativo')
        quantidade = request.form.get('quantidade')
        valor_unitario = request.form.get('valor_unitario')
        tipo_operacao = request.form.get('tipo_operacao')
        
        sucesso, resultado = controller.cadastrar_operacao(data, ativo, quantidade, valor_unitario, tipo_operacao)
        
        if sucesso:
            flash(resultado, 'success')
            return redirect(url_for('operacao.listar'))
        else:
            for erro in resultado:
                flash(erro, 'danger')
                
    return render_template('cadastrar.html')

# Rota para ver os detalhes de uma operação específica
@operacao_bp.route('/detalhar/<int:id>')
def detalhar(id):
    operacao = controller.buscar_por_id(id)
    if not operacao:
        flash("Operação não encontrada.", "danger")
        return redirect(url_for('operacao.listar'))
    return render_template('detalhar.html', operacao=operacao)

# Rota para atualizar uma operação existente
@operacao_bp.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    operacao = controller.buscar_por_id(id)
    if not operacao:
        flash("Operação não encontrada.", "danger")
        return redirect(url_for('operacao.listar'))

    if request.method == 'POST':
        data = request.form.get('data')
        ativo = request.form.get('ativo')
        quantidade = request.form.get('quantidade')
        valor_unitario = request.form.get('valor_unitario')
        tipo_operacao = request.form.get('tipo_operacao')
        
        sucesso, resultado = controller.atualizar_operacao(id, data, ativo, quantidade, valor_unitario, tipo_operacao)
        
        if sucesso:
            flash(resultado, 'success')
            return redirect(url_for('operacao.listar'))
        else:
            for erro in resultado:
                flash(erro, 'danger')

    return render_template('atualizar.html', operacao=operacao)

# Rota para excluir uma operação
@operacao_bp.route('/excluir/<int:id>', methods=['POST', 'GET'])
def excluir(id):
    controller.excluir_operacao(id)
    flash("Operação excluída com sucesso!", "success")
    return redirect(url_for('operacao.listar'))