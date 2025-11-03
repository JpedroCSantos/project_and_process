from typing import Optional
from datetime import datetime
from pydantic import Field, BaseModel, EmailStr, PositiveFloat, PositiveInt, field_validator
from src.utils.loader import VENDEDORES_ATIVOS

class Vendas(BaseModel):
    data_da_venda: datetime = Field(alias="Data da Venda")
    nome_do_cliente: str = Field(alias="Nome do Cliente")
    nome_do_vendedor: str = Field(alias="Nome do Vendedor")
    empresas: str = Field(alias="Empresas")
    duracao_do_projeto_meses: PositiveInt = Field(alias="Duracao do Projeto (meses)")
    valor_total_do_projeto_tcv: PositiveFloat = Field(alias="Valor Total do Projeto (TCV)")
    comissao_do_vendedor: PositiveFloat = Field(alias="Comissao do Vendedor")
    valor_da_parcela: PositiveFloat = Field(alias="Valor da Parcela (1 parcela)")
    valor_do_caixa: float = Field(alias="Valor do Caixa (apos 1 parcela)")
    valor_p_marketing: PositiveFloat = Field(alias="Valor p/ Marketing")
    pago: str = Field(alias="Pago?")
    observacoes: Optional[str] = Field(alias="Observacoes", default=None)

    @field_validator('pago')
    @classmethod
    def validar_pagamento(cls, value: str) -> str:
        """
        Valida se o projeto está pago ou não, se "Sim" retorna True,
        Se não retorna False.
        Caso contrário retorna Error.
        """
        if value.lower() == 'sim':
            return True
        elif value.lower() == 'não' or value.lower() == 'nao':
            return False
        else:
            raise ValueError
        
    @field_validator('nome_do_vendedor')
    @classmethod
    def validar_vendedor(cls, vendedor: str) -> str:
        """
        Valida se o projeto está pago ou não, se "Sim" retorna True,
        Se não retorna False.
        Caso contrário retorna Error.
        """
        if vendedor not in VENDEDORES_ATIVOS:
            raise ValueError(f"Vendedor '{vendedor}' não está cadastrado ou ativo.")
        
        return vendedor