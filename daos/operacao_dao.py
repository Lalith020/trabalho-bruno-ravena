# sqlite3 é a ferramenta nativa do Python para conversar com o banco SQLite.
import sqlite3

# O DAO transforma as linhas do banco em objetos Operacao e vice-versa.
from models.operacao import Operacao

class OperacaoDAO:
    # O DAO é o arquivista da Batcaverna: guarda e recupera os dados das operações.
    def __init__(self, db_name="corretora.db"):
        self.db_name = db_name
        self.criar_tabela()

    # Abre uma conexão com o arquivo do banco de dados.
    def conectar(self):
        return sqlite3.connect(self.db_name)

    # Prepara a tabela uma única vez; se já existir, mantém os dados que estão lá.
    def criar_tabela(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                ativo TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_unitario REAL NOT NULL,
                tipo_operacao TEXT NOT NULL,
                valor_bruto REAL NOT NULL,
                taxas REAL NOT NULL,
                valor_liquido REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    # Salva uma operação nova. Os ? recebem valores separados para evitar montar SQL na mão.
    def inserir(self, operacao):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO operacoes (data, ativo, quantidade, valor_unitario, tipo_operacao, valor_bruto, taxas, valor_liquido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (operacao.data, operacao.ativo, operacao.quantidade, operacao.valor_unitario, 
              operacao.tipo_operacao, operacao.valor_bruto, operacao.taxas, operacao.valor_liquido))
        conn.commit()
        conn.close()

    # Busca todas as linhas e monta uma lista de objetos Operacao.
    def listar_todos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, data, ativo, quantidade, valor_unitario, tipo_operacao, valor_bruto, taxas, valor_liquido FROM operacoes")
        linhas = cursor.fetchall()
        conn.close()

        operacoes = []
        for linha in linhas:
            op = Operacao(
                data=linha[1],
                ativo=linha[2],
                quantidade=linha[3],
                valor_unitario=linha[4],
                tipo_operacao=linha[5],
                id=linha[0]
            )
            op.valor_bruto = linha[6]
            op.taxas = linha[7]
            op.valor_liquido = linha[8]
            operacoes.append(op)
        return operacoes

    # Busca uma operação específica pelo ID
    def buscar_por_id(self, operacao_id):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, data, ativo, quantidade, valor_unitario, tipo_operacao, valor_bruto, taxas, valor_liquido FROM operacoes WHERE id = ?", (operacao_id,))
        linha = cursor.fetchone()
        conn.close()

        if linha:
            op = Operacao(
                data=linha[1],
                ativo=linha[2],
                quantidade=linha[3],
                valor_unitario=linha[4],
                tipo_operacao=linha[5],
                id=linha[0]
            )
            op.valor_bruto = linha[6]
            op.taxas = linha[7]
            op.valor_liquido = linha[8]
            return op
        return None

    # Pesquisa operações pelo código do ativo
    def buscar_por_ativo(self, ativo):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, data, ativo, quantidade, valor_unitario, tipo_operacao, valor_bruto, taxas, valor_liquido FROM operacoes WHERE ativo LIKE ?", (f"%{ativo.upper()}%",))
        linhas = cursor.fetchall()
        conn.close()

        operacoes = []
        for linha in linhas:
            op = Operacao(
                data=linha[1],
                ativo=linha[2],
                quantidade=linha[3],
                valor_unitario=linha[4],
                tipo_operacao=linha[5],
                id=linha[0]
            )
            op.valor_bruto = linha[6]
            op.taxas = linha[7]
            op.valor_liquido = linha[8]
            operacoes.append(op)
        return operacoes

    # Pesquisa operações por intervalo de datas
    def buscar_por_intervalo_datas(self, data_inicio, data_fim):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, data, ativo, quantidade, valor_unitario, tipo_operacao, valor_bruto, taxas, valor_liquido FROM operacoes WHERE data BETWEEN ? AND ?", (data_inicio, data_fim))
        linhas = cursor.fetchall()
        conn.close()

        operacoes = []
        for linha in linhas:
            op = Operacao(
                data=linha[1],
                ativo=linha[2],
                quantidade=linha[3],
                valor_unitario=linha[4],
                tipo_operacao=linha[5],
                id=linha[0]
            )
            op.valor_bruto = linha[6]
            op.taxas = linha[7]
            op.valor_liquido = linha[8]
            operacoes.append(op)
        return operacoes

    # Atualiza uma operação existente (mantendo o ID intacto)
    def atualizar(self, operacao):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE operacoes 
            SET data = ?, ativo = ?, quantidade = ?, valor_unitario = ?, tipo_operacao = ?, valor_bruto = ?, taxas = ?, valor_liquido = ?
            WHERE id = ?
        """, (operacao.data, operacao.ativo, operacao.quantidade, operacao.valor_unitario, 
              operacao.tipo_operacao, operacao.valor_bruto, operacao.taxas, operacao.valor_liquido, operacao.id))
        conn.commit()
        conn.close()

    # Exclui uma operação pelo ID
    def excluir(self, operacao_id):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM operacoes WHERE id = ?", (operacao_id,))
        conn.commit()
        conn.close()