# Ferramentas do Flask para ler formulários, mostrar páginas e redirecionar o usuário.
from flask import render_template, request, redirect, url_for, flash

# A rota conversa com o controller, que cuida das regras antes de acessar o banco.
from controllers.operacao_controller import OperacaoController

# Uma central de atendimento: todas as rotas usam este controller.
controller = OperacaoController()

# Página inicial: escolhe o tipo de busca ou lista tudo, como um menu de missões.
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

# Recebe o formulário e pede ao controller para validar e cadastrar.
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
            return redirect(url_for('listar'))
        else:
            for erro in resultado:
                flash(erro, 'danger')

    return render_template('cadastrar.html')

# Busca uma operação pelo ID e mostra sua ficha, como abrir o perfil de um personagem.
def detalhar(id):
    operacao = controller.buscar_por_id(id)
    if not operacao:
        flash("Operação não encontrada.", "danger")
        return redirect(url_for('listar'))
    return render_template('detalhar.html', operacao=operacao)

# Carrega a operação e, no envio do formulário, pede ao controller para atualizá-la.
def atualizar(id):
    operacao = controller.buscar_por_id(id)
    if not operacao:
        flash("Operação não encontrada.", "danger")
        return redirect(url_for('listar'))

    if request.method == 'POST':
        data = request.form.get('data')
        ativo = request.form.get('ativo')
        quantidade = request.form.get('quantidade')
        valor_unitario = request.form.get('valor_unitario')
        tipo_operacao = request.form.get('tipo_operacao')

        sucesso, resultado = controller.atualizar_operacao(id, data, ativo, quantidade, valor_unitario, tipo_operacao)

        if sucesso:
            flash(resultado, 'success')
            return redirect(url_for('listar'))
        else:
            for erro in resultado:
                flash(erro, 'danger')

    return render_template('atualizar.html', operacao=operacao)

# Pede ao controller para excluir a operação indicada pelo ID.
def excluir(id):
    controller.excluir_operacao(id)
    flash("Operação excluída com sucesso!", "success")
    return redirect(url_for('listar'))


# Registra cada endereço no Flask: este mapa conecta URLs às funções certas.
def registrar_rotas(app):
    app.add_url_rule('/', view_func=listar)
    app.add_url_rule('/cadastrar', view_func=cadastrar, methods=['GET', 'POST'])
    app.add_url_rule('/detalhar/<int:id>', view_func=detalhar)
    app.add_url_rule('/atualizar/<int:id>', view_func=atualizar, methods=['GET', 'POST'])
    app.add_url_rule('/excluir/<int:id>', view_func=excluir, methods=['GET', 'POST'])