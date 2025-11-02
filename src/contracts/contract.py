from datetime import datetime
from pydantic import BaseModel, EmailStr, PositiveFloat, PositiveInt, field_validator
from src.utils.loader import CATEGORIAS_VALIDAS

class Vendas(BaseModel):
    email: EmailStr
    data: datetime
    valor: PositiveFloat
    produto: str
    quantidade: PositiveInt
    categoria: str

    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, category: str) -> str:
        """
        Valida se a categoria (category) recebida está presente no set 
        CATEGORIAS_VALIDAS que foi carregado do CSV.
        """
        if category not in CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoria '{category}' não é uma categoria válida.")
        
        return category