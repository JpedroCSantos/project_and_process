import pandas as pd
from typing import Optional, Any
from datetime import datetime, date
from pydantic import Field, BaseModel, EmailStr, PositiveFloat, PositiveInt, field_validator
from src.utils.loader import VENDEDORES_ATIVOS

class Vendas(BaseModel):
    Data_Venda: datetime = Field(alias="Data da Venda")
    Nome_Cliente: str = Field(alias="Nome do Cliente")
    Nome_Vendedor: str = Field(alias="Nome do Vendedor")
    Empresa: str = Field(alias="Empresas")
    Duracao_Projeto_meses: PositiveInt = Field(alias="Duracao do Projeto (meses)")
    Valor_Total_Projeto: PositiveFloat = Field(alias="Valor Total do Projeto (TCV)")
    Comissao_Vendedor: PositiveFloat = Field(alias="Comissao do Vendedor")
    Valor_primeira_Parcela: PositiveFloat = Field(alias="Valor da Parcela (1 parcela)")
    Valor_Caixa_pos_Primeira_Parcela: float = Field(alias="Valor do Caixa (apos 1 parcela)")
    Valor_Marketing: PositiveFloat = Field(alias="Valor p/ Marketing")
    Pago: bool = Field(alias="Pago?")
    Observacoes: Optional[str] = Field(alias="Observacoes", default=None)

    @field_validator('Pago', mode='before')
    @classmethod
    def validar_pagamento(cls, value: str) -> bool:
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
        
    @field_validator('Nome_Vendedor')
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
    

    @field_validator('Data_Venda', mode='before')
    @classmethod
    def parsear_data(cls, v: Any) -> date:
        """
        Converte string brasileira (DD/MM/YYYY) para objeto date (YYYY-MM-DD).
        """
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()
            except ValueError:
                raise ValueError(f"Formato de data inválido: '{v}'. Esperado DD/MM/YYYY")
        if isinstance(v, datetime):
            return v.date()       
        if isinstance(v, date):
            return v
        
        raise ValueError(f"Tipo de data inesperado: {type(v)}")
    
    @field_validator('Observacoes', mode='before')
    @classmethod
    def converter_nan_para_none(cls, v: Any) -> Optional[str]:
        """
        Pega o valor 'cru' (modo 'before'). Se for 'nan' (que o pandas lê 
        como float), converte para None.
        """
        if pd.isna(v):
            return None
        
        return v
    
    @field_validator(
        'Valor_Total_Projeto',
        'Comissao_Vendedor',
        'Valor_primeira_Parcela',
        'Valor_Caixa_pos_Primeira_Parcela',
        'Valor_Marketing',
        mode='before'
    )
    @classmethod
    def converter_virgula_para_ponto(cls, v: Any) -> float:
        if isinstance(v, str):
            v = v.replace(',', '.')
        
        try:
            return round(float(v), 2)
        except (ValueError, TypeError):
             raise ValueError(f"Valor numérico inválido: {v}")