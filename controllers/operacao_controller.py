from models.operacao import Operacao
from dao.operacao_dao import OperacaoDAO
from datetime import datetime
import re

class OperacaoController:
    def __init__(self):
        self.dao = OperacaoDAO()

    def listar_operacoes(self):
        return self.dao.listar_todos()

    def cadastrar_operacao(self, data, ativo, quantidade, valor_unitario, tipo_operacao):
        erros = []

        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            erros.append("A data informada não é válida.")

        ativo_limpo = ativo.upper().strip() if ativo else ""
        if not re.match(r'^[A-Z]{4}[0-9]{1,2}$', ativo_limpo):
            erros.append("O código do ativo deve conter exatamente 4 letras maiúsculas seguidas de 1 ou 2 números (Ex: PETR4, VALE3).")

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

        nova_op = Operacao(
            data=data,
            ativo=ativo_limpo,
            quantidade=int(quantidade),
            valor_unitario=float(valor_unitario),
            tipo_operacao=tipo_limpo
        )

        self.dao.inserir(nova_op)
        return True, "Operação cadastrada com sucesso!"