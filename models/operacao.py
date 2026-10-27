import re
from datetime import datetime

class Operacao:
    def __init__(self, data, ativo, quantidade, valor_unitario, tipo_operacao, id=None):
        self.id = id
        self.data = data
        self.ativo = ativo.upper().strip() if ativo else ""
        self.quantidade = int(quantidade) if quantidade else 0
        self.valor_unitario = float(valor_unitario) if valor_unitario else 0.0
        self.tipo_operacao = tipo_operacao.lower().strip() if tipo_operacao else ""

        self.valor_bruto = self.quantidade * self.valor_unitario
        self.taxas = self.valor_bruto * 0.0003  # 0,03%
        
        if self.tipo_operacao == "compra":
            self.valor_liquido = self.valor_bruto + self.taxas
        elif self.tipo_operacao == "venda":
            self.valor_liquido = self.valor_bruto - self.taxas
        else:
            self.valor_liquido = 0.0
