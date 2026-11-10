from models.operacao import Operacao
from daos.operacao_dao import OperacaoDAO
from datetime import datetime
import re

class OperacaoController:
    # Como Nick Fury, coordena as regras e chama o DAO quando precisa falar com o banco.
    def __init__(self):
        self.dao = OperacaoDAO()

    # Pede ao DAO todas as operações cadastradas.
    def listar_operacoes(self):
        return self.dao.listar_todos()

    # Pede ao DAO a operação que corresponde a este ID.
    def buscar_por_id(self, operacao_id):
        return self.dao.buscar_por_id(operacao_id)

    # Evita uma busca vazia e procura pelo código do ativo.
    def pesquisar_por_ativo(self, ativo):
        if not ativo:
            return []
        return self.dao.buscar_por_ativo(ativo)

    # Procura operações dentro do período informado.
    def pesquisar_por_datas(self, data_inicio, data_fin):
        if not data_inicio or not data_fin:
            return []
        return self.dao.buscar_por_intervalo_datas(data_inicio, data_fin)

    # Confere os dados antes de salvar: é o controle de segurança na entrada da missão.
    def cadastrar_operacao(self, data, ativo, quantidade, valor_unitario, tipo_operacao):
        erros = []

        # Exige o formato ano-mês-dia, para a data não virar uma charada.
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            erros.append("A data informada não é válida.")

        # Padroniza o código e confere o formato esperado, como validar o crachá antes de entrar.
        ativo_limpo = ativo.upper().strip() if ativo else ""
        if not re.match(r'^[A-Z]{4}[0-9]{1,2}$', ativo_limpo):
            erros.append("O código do ativo deve conter exatamente 4 letras maiúsculas seguidas de 1 ou 2 números (Ex: PETR4, VALE3).")

        # Só aceita quantidade inteira e positiva.
        try:
            qtd = int(quantidade)
            if qtd <= 0:
                erros.append("A quantidade deve ser um número inteiro positivo.")
        except (ValueError, TypeError):
            erros.append("A quantidade deve ser um número inteiro válido.")

        # Só aceita preço numérico e maior que zero.
        try:
            val_unit = float(valor_unitario)
            if val_unit <= 0:
                erros.append("O valor unitário deve ser positivo.")
        except (ValueError, TypeError):
            erros.append("O valor unitário deve ser um número válido.")

        # Padroniza e aceita apenas compra ou venda.
        tipo_limpo = tipo_operacao.lower().strip() if tipo_operacao else ""
        if tipo_limpo not in ["compra", "venda"]:
            erros.append("O tipo de operação deve ser 'compra' ou 'venda'.")

        if erros:
            return False, erros

        # Monta a ficha da operação com os dados já validados e padronizados.
        nova_op = Operacao(
            data=data,
            ativo=ativo_limpo,
            quantidade=int(quantidade),
            valor_unitario=float(valor_unitario),
            tipo_operacao=tipo_limpo
        )

        self.dao.inserir(nova_op)
        return True, "Operação cadastrada com sucesso!"

    # Atualiza uma operação usando as mesmas regras de validação do cadastro.
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