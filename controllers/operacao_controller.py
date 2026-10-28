from models.operacao import Operacao
from dao.operacao_dao import OperacaoDAO
from datetime import datetime
import re

class OperacaoController:
    # Construtor da classe: inicializo o DAO aqui para conseguir usar os métodos do banco logo abaixo
    def __init__(self):
        self.dao = OperacaoDAO()

    # Função simples só para puxar e listar todas as operações cadastradas
    def listar_operacoes(self):
        return self.dao.listar_todos()

    # Busca uma operação específica pelo ID
    def buscar_por_id(self, operacao_id):
        return self.dao.buscar_por_id(operacao_id)

    # Pesquisa operações pelo código do ativo
    def pesquisar_por_ativo(self, ativo):
        if not ativo:
            return []
        return self.dao.buscar_por_ativo(ativo)

    # Pesquisa operações por intervalo de datas
    def pesquisar_por_datas(self, data_inicio, data_fin):
        if not data_inicio or not data_fin:
            return []
        return self.dao.buscar_por_intervalo_datas(data_inicio, data_fin)

    # Função de cadastro: valida tudo o que o usuário digita antes de mandar pra base de dados
    def cadastrar_operacao(self, data, ativo, quantidade, valor_unitario, tipo_operacao):
        erros = []

        # Checa se a data tá no formato certinho de ano-mês-dia
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            erros.append("A data informada não é válida.")

        # Deixa o código do ativo maiúsculo, tira espaços e valida o padrão da bolsa (ex: PETR4)
        ativo_limpo = ativo.upper().strip() if ativo else ""
        if not re.match(r'^[A-Z]{4}[0-9]{1,2}$', ativo_limpo):
            erros.append("O código do ativo deve conter exatamente 4 letras maiúsculas seguidas de 1 ou 2 números (Ex: PETR4, VALE3).")

        # Garante que a quantidade é um número inteiro e maior que zero
        try:
            qtd = int(quantidade)
            if qtd <= 0:
                erros.append("A quantidade deve ser um número inteiro positivo.")
        except (ValueError, TypeError):
            erros.append("A quantidade deve ser um número inteiro válido.")

        # Garante que o valor unitário é um número válido e positivo
        try:
            val_unit = float(valor_unitario)
            if val_unit <= 0:
                erros.append("O valor unitário deve ser positivo.")
        except (ValueError, TypeError):
            erros.append("O valor unitário deve ser um número válido.")

        # Padroniza o tipo pra minúsculo e só aceita 'compra' ou 'venda'
        tipo_limpo = tipo_operacao.lower().strip() if tipo_operacao else ""
        if tipo_limpo not in ["compra", "venda"]:
            erros.append("O tipo de operação deve ser 'compra' ou 'venda'.")

        if erros:
            return False, erros

        # Cria o objeto da operação com os dados já tratados e limpos
        nova_op = Operacao(
            data=data,
            ativo=ativo_limpo,
            quantidade=int(quantidade),
            valor_unitario=float(valor_unitario),
            tipo_operacao=tipo_limpo
        )

        self.dao.inserir(nova_op)
        return True, "Operação cadastrada com sucesso!"

    # Atualiza uma operação existente com validações idênticas às do cadastro
    def atualizar_operacao(self, operacao_id, data, ativo, quantidade, valor_unitario, tipo_operacao):
        erros = []

        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            erros.append("A data informada não é válida.")

        ativo_limpo = ativo.upper().strip() if ativo else ""
        if not re.match(r'^[A-Z]{4}[0-9]{1,2}$', ativo_limpo):
            erros.append("O código do ativo deve conter exatamente 4 letras maiúsculas seguidas de 1 ou 2 números.")

        try:
            qtd = int(quantidade)
            if qtd <= 0:
                erros.append("A quantidade deve ser um número inteiro positivo.")
        except (ValueError, TypeError):
            erros.append("A quantidade deve ser um número inteiro válido.")

        try:
            val_unit = float(valor_unitario)
            if val_unit <= 0:
                erros.append("O valor unitário deve ser positivo.")
        except (ValueError, TypeError):
            erros.append("O valor unitário deve ser um número válido.")

        tipo_limpo = tipo_operacao.lower().strip() if tipo_operacao else ""
        if tipo_limpo not in ["compra", "venda"]:
            erros.append("O tipo de operação deve ser 'compra' ou 'venda'.")

        if erros:
            return False, erros

        op_atualizada = Operacao(
            data=data,
            ativo=ativo_limpo,
            quantidade=int(quantidade),
            valor_unitario=float(valor_unitario),
            tipo_operacao=tipo_limpo,
            id=operacao_id
        )

        self.dao.atualizar(op_atualizada)
        return True, "Operação atualizada com sucesso!"

    # Exclui uma operação pelo ID
    def excluir_operacao(self, operacao_id):
        self.dao.excluir(operacao_id)
        return True, "Operação excluída com sucesso!"