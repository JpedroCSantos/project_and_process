import pandas as pd
import chardet

from datetime import datetime
from src.contracts.contract import Vendas 

class ExcelExtractor:
    def __init__(self, file):
        self.file = file
        self.df = None

    def extract(self):
        """
        Lê o arquivo (CSV ou Excel) detectando o encoding automaticamente.
        """
        try:
            if self.file.name.endswith('.csv'):
                raw_data = self.file.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                self.file.seek(0)
                self.df = pd.read_csv(self.file, sep=';', encoding=encoding)
            else:
                self.df = pd.read_excel(self.file)
            return self.df
            
        except Exception as e:
            raise ValueError(f"Falha crítica ao ler o arquivo: {e}")

    def validate_data(self):
        """
        Aplica o contrato Pydantic linha a linha.
        Retorna: (is_valid: bool, error_list: list[dict])
        """
        if self.df is None:
            return False, [{"Linha": "N/A", "Erro": "Nenhum arquivo carregado."}]

        error_list = []
        dados_limpos = []
        for index, row in self.df.iterrows():
            try:
                venda_validada = Vendas(**row.to_dict())          
                dados_limpos.append(venda_validada.model_dump())
                
            except Exception as e:
                error_list.append({
                    "Linha": index + 2,
                    "Erro": str(e)
                })
        if error_list:
            return False, error_list
        self.df = pd.DataFrame(dados_limpos)
        
        return True, []

    def get_errors_as_df(self, error_list):
        """
        Converte a lista de dicionários de erro em um DataFrame para visualização.
        """
        if not error_list:
            return pd.DataFrame()
            
        erros_df = pd.DataFrame(error_list)
        
        if "Linha" in erros_df.columns:
            return erros_df.set_index("Linha")
            
        return erros_df

    def process_file(self):
        """
        Orquestrador principal.
        Retorna: (df, result, error_list)
        """
        try:
            self.extract()
            
        except ValueError as e:
            return None, False, [{"Linha": "Arquivo", "Erro": str(e)}]
        except Exception as e:
            return None, False, [{"Linha": "Arquivo", "Erro": f"Erro inesperado: {e}"}]

        is_valid, error_list = self.validate_data()
        
        return self.df, is_valid, error_list