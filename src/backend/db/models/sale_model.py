from sqlalchemy import Column, DateTime, Float, Integer, Numeric, String, BigInteger, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Sale(Base):
    __tablename__ = 'sales'                 # Nome da tabela no banco
    __table_args__ = {'schema': 'public'}   # Schema no banco

    id = Column(BigInteger, primary_key=True, index=True)
    Data_Venda = Column(DateTime, nullable=False)
    Nome_Cliente = Column(String, nullable=False)
    Nome_Vendedor = Column(String, nullable=False)
    Empresa = Column(String, nullable=False)
    Duracao_Projeto_meses = Column(Integer, nullable=False)
    Valor_Total_Projeto = Column(Numeric(10, 2), nullable=False)
    Comissao_Vendedor = Column(Numeric(10, 2), nullable=False)
    Valor_primeira_Parcela = Column(Numeric(10, 2), nullable=False)
    Valor_Caixa_pos_Primeira_Parcela = Column(Numeric(10, 2), nullable=False)
    Valor_Marketing = Column(Float, nullable=False)
    Pago = Column(Boolean, nullable=False)
    Observacoes = Column(String)   
    created_at = Column(DateTime, default=func.now())
    