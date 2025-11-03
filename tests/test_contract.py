import pytest

from typing import Optional
from datetime import datetime
from pydantic import ValidationError
from src.contracts.contract import Vendas

def test_vendas_com_dados_validos():
    dados_validos = {
        "Data da Venda": datetime.now(),
        "Nome do Cliente": "João",
        "Nome do Vendedor": "Maria",
        "Empresas": "Empresa A",
        "Duracao do Projeto (meses)": 6,
        "Valor Total do Projeto (TCV)": 100000,
        "Comissao do Vendedor": 1000,
        "Valor da Parcela (1 parcela)": 10000,
        "Valor do Caixa (apos 1 parcela)": 90000,
        "Valor p/ Marketing": 10000,
        "Pago?": "Não",
        "Observacoes": "Observações adicionais"
    }

    venda = Vendas(**dados_validos)

    assert venda.data_da_venda == dados_validos["Data da Venda"]
    assert venda.nome_do_cliente == dados_validos["Nome do Cliente"]
    assert venda.nome_do_vendedor == dados_validos["Nome do Vendedor"]
    assert venda.empresas == dados_validos["Empresas"]
    assert venda.duracao_do_projeto_meses == dados_validos["Duracao do Projeto (meses)"]
    assert venda.valor_total_do_projeto_tcv == dados_validos["Valor Total do Projeto (TCV)"]
    assert venda.comissao_do_vendedor == dados_validos["Comissao do Vendedor"]
    assert venda.valor_da_parcela == dados_validos["Valor da Parcela (1 parcela)"]
    assert venda.valor_do_caixa == dados_validos["Valor do Caixa (apos 1 parcela)"]
    assert venda.valor_p_marketing == dados_validos["Valor p/ Marketing"]
    assert venda.pago == (True if dados_validos["Pago?"] == "Sim" else False)
    assert venda.observacoes == dados_validos["Observacoes"]

def test_vendas_com_dados_invalidos():
    dado_invalidos = {
        "Data da Venda": "12/12/2023",
        "Nome do Cliente": 456,
        "Nome do Vendedor": 123,
        "Empresas": 12,
        "Duracao do Projeto (meses)": 6,
        "Valor Total do Projeto (TCV)": -100000,
        "Comissao do Vendedor": -1000,
        "Valor da Parcela (1 parcela)": -10000,
        "Valor do Caixa (apos 1 parcela)": '',
        "Valor p/ Marketing": 10000,
        "Pago?": False,
        "Observacoes": ""
    }

    with pytest.raises(ValidationError):
        Vendas(**dado_invalidos)

def test_vendedor_invalido():
    dado_invalidos = {
        "Data da Venda": datetime.now(),
        "Nome do Cliente": "João",
        "Nome do Vendedor": "Mariaah",
        "Empresas": "Empresa A",
        "Duracao do Projeto (meses)": 6,
        "Valor Total do Projeto (TCV)": 100000,
        "Comissao do Vendedor": 1000,
        "Valor da Parcela (1 parcela)": 10000,
        "Valor do Caixa (apos 1 parcela)": 90000,
        "Valor p/ Marketing": 10000,
        "Pago?": "Não",
        "Observacoes": "Observações adicionais"
    }

    with pytest.raises(ValidationError):
        Vendas(**dado_invalidos)