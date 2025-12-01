import pandas as pd

from datetime import datetime
from src.config.config import settings
from src.backend.db.classes.db_class import PostgresService
from src.backend.db.models.sale_model import Sale

def send_dataframe_to_database(df: pd.DataFrame) -> str:
    """
    Carrega DataFrame para tabela PostgreSQL.
    
    :param df: DataFrame a ser enviado ao banco de dados
    :type df: pd.DataFrame
    :return: Mensagem de sucesso ou erro.
    :rtype: str
    """
    
    with PostgresService(settings.dev_db_params) as db:
        db.full_refresh_table()
        df['created_at'] = datetime.now()
        db.bulk_insert_data(df, Sale.__tablename__)
        return db.error
