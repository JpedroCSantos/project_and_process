import pytest

from typing import Optional
from datetime import datetime
from pydantic import ValidationError
from src.contracts.contract import Vendas

def test_vendas_com_dados_validos():

    dados_validos = {
        "email": "comprador@example.com",
        "data": datetime.now(),
        "valor": 100.50,
        "produto": "Produto X",
        "quantidade": 3,
        "categoria": "Categoria 1",
    }

    venda = Vendas(**dados_validos)

    assert venda.email == dados_validos["email"]
    assert venda.data == dados_validos["data"]
    assert venda.valor == dados_validos["valor"]
    assert venda.produto == dados_validos["produto"]
    assert venda.quantidade == dados_validos["quantidade"]
    assert venda.categoria == dados_validos["categoria"]

def test_vendas_com_dados_invalidos():
    dado_invalidos = {
        "email": "comprador",
        "data": "não é uma data",
        "valor": -100,
        "produto": "",
        "quantidade": -1,
        "categoria": "categoria1"
    }

    with pytest.raises(ValidationError):
        Vendas(**dado_invalidos)

def test_email_invalido():
    dado_invalidos = {
        "email": "comprador",
        "data": datetime.now(),
        "valor": 100,
        "produto": "Produto X",
        "quantidade": 1,
        "categoria": "Categoria 1"
    }

    with pytest.raises(ValidationError):
        Vendas(**dado_invalidos)

def test_validacao_categoria():
    data = {
        "email": "comprador@example.com",
        "data": datetime.now(),
        "valor": 100.50,
        "produto": "Produto X",
        "quantidade": 1,
        "categoria": 123,
    }

    with pytest.raises(ValidationError):
        Vendas(**data)