import os
import sys
import psycopg2
import pandas as pd

from loguru import logger
from typing import Dict, Optional
from contextlib import contextmanager
from src.config.logger import get_bound_logger
from sqlalchemy import create_engine
from src.backend.db.models.sale_model import Base, Sale
from psycopg2.extras import execute_values

class PostgresService():
    def __init__(self, config: Optional[str] = None):
        self.params = self.get_db_params(config)
        self._connection = None
        self.cursor = None
        self._is_connected = False
        self.error = None
        self.connection_string = self.build_connection_string(config)
        self.logger = get_bound_logger(
            host= config["host"],
            database= config["dbname"]
        )

    def __enter__(self):
        """Suporte a context manager"""
        self.connect_db()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup automático no context manager"""
        self.disconnect_db()

    def __del__(self):
        """Cleanup no destructor"""
        if hasattr(self, '_connection'):
            self.disconnect_db()

    def get_db_params(self, config: Optional[str] = None) -> Dict:
        return {
            "host": config["host"],
            "port": config["port"],
            "dbname": config["dbname"],
            "user": config["user"],
            "password": config["password"]
        }
    
    def build_connection_string(self, config: Optional[str] = None) -> Dict:
        return f'postgresql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["dbname"]}'
    
    def connect_db(self) -> str:
        if self._is_connected:
            logger.info("Conexão já está ativa")
            return
        
        try:
            logger.info("Conectando ao banco de dados PostgreSQL...")
            self._connection = psycopg2.connect(**self.params)
            self._connection.autocommit = False 
            self._is_connected = True

            with self._connection.cursor() as cur:
                cur.execute("SELECT version();")
                db_version = cur.fetchone()
                logger.success(f"Conectado com sucesso! Versão: {db_version[0]}")
            logger.success("Conexão estabelecida com sucesso")
            return
        
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            logger.warning(f"Falha de conexão: {e}.")
            self.check_error()
            self.error += f"{e}\n"
            
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"Erro ao conectar ou operar no PostgreSQL: {e}")
            self.check_error()
            self.error += f"{e}\n"

    def ensure_connection(self):
        """Garante que a conexão está ativa, reconecta se necessário"""
        if not self._is_connected:
            logger.warning("Conexão perdida, reconectando...")
            self.disconnect_db() 
            self.connect_db()

    def disconnect_db(self):
        """Fecha a conexão com o banco"""
        if self._connection and self._is_connected:
            self._connection.close()
            self._is_connected = False
            logger.info("Conexão com PostgreSQL fechada")
    
    @contextmanager
    def get_cursor(self, commit=True):
        """Context manager para operações com cursor"""
        self.ensure_connection()
        cursor = self._connection.cursor()
        try:
            yield cursor
            if commit:
                self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            logger.error(f"Erro na operação do banco: {e}")
            self.check_error()
            self.error += f"{e}\n"
        finally:
            cursor.close()
    
    def execute_query(self, query: str, params=None, fetch=False):
        """Executa uma query e opcionalmente retorna resultados"""
        self.ensure_connection()
        with self.get_cursor() as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
        
    def full_refresh_table(self):
        """Usa SQLAlchemy APENAS para recriar a tabela baseada no Model"""
        logger.info(f"Criando tabelas pelo sqlalchemy")
        try:
            engine = create_engine(self.connection_string)
            
            Base.metadata.drop_all(engine, tables=[Sale.__table__])
            Base.metadata.create_all(engine, tables=[Sale.__table__])
            engine.dispose()
        
        except Exception as e:
            logger.warning(f"Não foi possível criar tabelas pelo sqlalchemy: {e}")
            self.check_error()
            self.error += f"{e}\n"

    def bulk_insert_data(self, df, table_name: str, schema: str = "public", unique_columns: list = None):
        """
        Insere dados de um DataFrame no banco de forma otimizada.
        
        Args:
            df (pd.DataFrame): DataFrame
            schema (str): Schema do banco (ex: 'silver').
            table_name (str): Nome da tabela.
            unique_columns (list): Lista de colunas que formam a chave única (para evitar duplicatas).
        """
        columns = list(df.columns)
        values = [tuple(x) for x in df.where(pd.notnull(df), None).to_numpy()]
        cols_str = ', '.join([f'"{col}"' for col in columns])
        on_conflict_clause = ""
        if unique_columns:
            unique_cols_str = ', '.join([f'"{col}"' for col in unique_columns])
            on_conflict_clause = f"ON CONFLICT ({unique_cols_str}) DO NOTHING"

        query = f"""
            INSERT INTO {schema}.{table_name} ({cols_str})
            VALUES %s
            {on_conflict_clause}
        """
        with self.get_cursor() as cur:
            try:
                execute_values(
                    cur, 
                    query, 
                    values, 
                    template=None, 
                    page_size=1000 
                )
                logger.success(f"Carga finalizada. {len(values)} registros processados em {schema}.{table_name}.")
            except Exception as e:
                logger.error(f"Erro no Bulk Insert: {e}")
                self.check_error()
                self.error += f"{e}\n"

    def check_error(self):
        if self.error is None:
            self.error = ""