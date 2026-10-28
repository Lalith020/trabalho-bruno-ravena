# Importa a biblioteca de expressões regulares (caso precise de validar algum padrão aqui dentro)
import re

# Importa a biblioteca datetime para manipulação de datas
from datetime import datetime

class Operacao:
    # Construtor da classe: inicializa os dados da operação e já calcula os valores financeiros automáticos
    def __init__(self, data, ativo, quantidade, valor_unitario, tipo_operacao, id=None):
        self.id = id
        self.data = data
        self.ativo = ativo.upper().strip() if ativo else ""
        self.quantidade = int(quantidade) if quantidade else 0
        self.valor_unitario = float(valor_unitario) if valor_unitario else 0.0
        self.tipo_operacao = tipo_operacao.lower().strip() if tipo_operacao else ""

        # Calcula o valor bruto multiplicando a quantidade pelo preço unitário
        self.valor_bruto = self.quantidade * self.valor_unitario
        # Calcula as taxas aplicadas sobre o valor bruto (0,03%)
        self.taxas = self.valor_bruto * 0.0003  # 0,03%
        
        # Define o valor líquido somando as taxas no caso de compra ou subtraindo no caso de venda
        if self.tipo_operacao == "compra":
            self.valor_liquido = self.valor_bruto + self.taxas
        elif self.tipo_operacao == "venda":
            self.valor_liquido = self.valor_bruto - self.taxas
        else:
            self.valor_liquido = 0.0