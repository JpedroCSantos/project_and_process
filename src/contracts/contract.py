import pandas as pd
from typing import Optional, Any
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
    

    @field_validator('data_da_venda', mode='before')
    @classmethod
    def parsear_data_br(cls, v: Any) -> datetime:
        """
        Pega a string de data 'crua' (modo 'before') e a converte
        do formato DD/MM/YYYY para um objeto datetime.
        """
        if isinstance(v, str):
            try:
                # Tenta converter do formato brasileiro
                return datetime.strptime(v, '%d/%m/%Y')
            except ValueError:
                # Se falhar, levanta um erro claro
                raise ValueError(f"Formato de data inválido: '{v}'. Esperado DD/MM/YYYY")
        
        # Se já for um datetime (em um re-processamento, por exemplo), apenas retorne
        if isinstance(v, datetime):
            return v
        
        raise ValueError(f"Valor de data inesperado: {v}")
    
    @field_validator('observacoes', mode='before')
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
        'valor_total_do_projeto_tcv',
        'comissao_do_vendedor',
        'valor_da_parcela',
        'valor_do_caixa',
        'valor_p_marketing',
        mode='before'
    )
    @classmethod
    def converter_virgula_para_ponto(cls, v: Any) -> Any:
        """
        Converte strings numéricas com vírgula decimal (formato BR) 
        para o formato com ponto (formato US/Python).
        """
        if isinstance(v, str):
            return v.replace(',', '.')
        
        return v