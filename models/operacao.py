# re permite conferir padrões de texto; datetime ajuda a trabalhar com datas.
import re

from datetime import datetime

class Operacao:
    # Model: a ficha de cada operação, como a tela de status de um personagem.
    def __init__(self, data, ativo, quantidade, valor_unitario, tipo_operacao, id=None):
        self.id = id
        self.data = data
        self.ativo = ativo.upper().strip() if ativo else ""
        self.quantidade = int(quantidade) if quantidade else 0
        self.valor_unitario = float(valor_unitario) if valor_unitario else 0.0
        self.tipo_operacao = tipo_operacao.lower().strip() if tipo_operacao else ""

        # Valor bruto: quantidade multiplicada pelo preço de cada unidade.
        self.valor_bruto = self.quantidade * self.valor_unitario
        # Taxa de 0,03% calculada sobre o valor bruto.
        self.taxas = self.valor_bruto * 0.0003  # 0,03%

        # Compra soma a taxa; venda desconta. O tipo define o cálculo final.
        if self.tipo_operacao == "compra":
            self.valor_liquido = self.valor_bruto + self.taxas
        elif self.tipo_operacao == "venda":
            self.valor_liquido = self.valor_bruto - self.taxas
        else:
            self.valor_liquido = 0.0