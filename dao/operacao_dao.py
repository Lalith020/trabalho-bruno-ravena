import sqlite3
from models.operacao import Operacao

class OperacaoDAO:
    def __init__(self, db_name="corretora.db"):
        self.db_name = db_name
        self.criar_tabela()

    def conectar(self):
        return sqlite3.connect(self.db_name)

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
