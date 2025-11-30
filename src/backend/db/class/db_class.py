import os
import sys
import psycopg2
import pandas as pd

from io import StringIO
from loguru import logger
from typing import Dict, Optional
from contextlib import contextmanager
from config.logger import get_bound_logger

class db_class():
    def __init__(self, config: Optional[str] = None):
        self.params = self.get_db_params(config)
        self._connection = None
        self.cursor = None
        self._is_connected = False

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
        
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as error:
            logger.warning(f"Falha de conexão: {error}.")
            

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Erro ao conectar ou operar no PostgreSQL: {error}")


    def disconnect_db(self):
        """Fecha a conexão com o banco"""
        if self._connection and self._is_connected:
            self._connection.close()
            self._is_connected = False
            logger.info("Conexão com PostgreSQL fechada")
    
    @contextmanager
    def get_cursor(self, commit=True):
        """Context manager para operações com cursor"""
        cursor = self._connection.cursor()
        try:
            yield cursor
            if commit:
                self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            logger.error(f"Erro na operação do banco: {e}")
        finally:
            cursor.close()
    
    def execute_query(self, query: str, params=None, fetch=False):
        """Executa uma query e opcionalmente retorna resultados"""
        with self.get_cursor() as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
