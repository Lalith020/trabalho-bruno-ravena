# Importa o modelo Operacao para estruturar os dados que vamos usar na corretora
from models.operacao import Operacao

# Importa o DAO da operação para fazer a ponte e salvar tudo no banco de dados SQLite
from dao.operacao_dao import OperacaoDAO

# Biblioteca padrão para mexer e validar datas
from datetime import datetime

# Biblioteca de expressões regulares para validar o formato dos ativos da bolsa
import re

class OperacaoController:
    # Construtor da classe: inicializo o DAO aqui para conseguir usar os métodos do banco logo abaixo
    def __init__(self):
        self.dao = OperacaoDAO()

    # Função simples só para puxar e listar todas as operações cadastradas
    def listar_operacoes(self):
        return self.dao.listar_todos()

    # Função de cadastro: valida tudo o que o usuário digita antes de mandar pra base de dados
    def cadastrar_operacao(self, data, ativo, quantidade, valor_unitario, tipo_operacao):
        # Lista vazia para guardar os erros de validação se houver algum
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

        # Se encontrou algum erro nas validações, para por aqui e retorna a lista de erros
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

        # Manda o DAO salvar de vez lá no SQLite
        self.dao.inserir(nova_op)
        return True, "Operação cadastrada com sucesso!"