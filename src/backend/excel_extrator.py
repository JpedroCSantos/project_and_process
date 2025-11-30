import pandas as pd
from src.contracts.contract import Vendas
from src.config.config import settings
from pydantic import ValidationError

def excel_to_df(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df


def csv_to_df(file):
    df = pd.read_csv(file, sep=';', encoding='latin1')
    return df    

def process_file(uploaded_file):
    try:
        error = None
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = excel_to_df(uploaded_file)
        elif uploaded_file.type == "text/csv":
            df = csv_to_df(uploaded_file)
    
        lista_de_aliases = [campo.alias for campo in Vendas.model_fields.values()]
        extra_cols = set(df.columns) - set(lista_de_aliases)

        if extra_cols:
            error = f"Colunas extras detectadas no Excel: {', '.join(extra_cols)}"
            return False, error, error

        erros_coletados = []
        for index, row in df.iterrows():
            try:
                _ = Vendas(**row.to_dict())
        
            except ValidationError as e:
                erros_da_linha = [f"**{err['loc'][0]}**: {err['msg']}" for err in e.errors()]
                
                erros_coletados.append({
                    "Linha": index + 2,
                    "Erros": "; ".join(erros_da_linha)
                })
                
            except Exception as e:
                erros_coletados.append({
                    "Linha": index + 2,
                    "Erros": str(e)
                })

        if len(erros_coletados):
            return df, False, erros_coletados

        return df, True, None

    except ValueError as ve:
        return df, False, str(ve)
    except Exception as e:
        return df, False, f"Erro inesperado: {str(e)}"
    
def process_erros_df(error):
    erros_df = pd.DataFrame(error).set_index("Linha")
    return erros_df