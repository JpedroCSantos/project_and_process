from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SaleSchema(BaseModel):
    Data_Venda: datetime
    Nome_Cliente: str
    Nome_Vendedor: str
    Empresa: str
    Duracao_Projeto_meses: int
    Valor_Total_Projeto: float
    Comissao_Vendedor: float
    Valor_primeira_Parcela: float
    Valor_Caixa_pos_Primeira_Parcela: float
    Valor_Marketing: float
    Pago: bool
    Observacoes: Optional[str]
