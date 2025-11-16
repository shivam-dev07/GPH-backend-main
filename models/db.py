"""
Database connection module
Handles MySQL connection with SSL for Aiven
"""

from contextlib import contextmanager
import pymysql
from pymysql.cursors import DictCursor
from config import DB_CONFIG
from utils.logger import logger


@contextmanager
def get_connection():
    """
    Context manager for database connections with SSL support.
    Configured for Aiven MySQL with required SSL mode.
    """
    connection = None
    try:
        # Add SSL configuration for Aiven
        ssl_config = DB_CONFIG.copy()
        ssl_config['ssl'] = {'ssl_mode': 'REQUIRED'}
        ssl_config['cursorclass'] = DictCursor
        
        connection = pymysql.connect(**ssl_config)
        yield connection
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()


def check_health():
    """Check database connection health"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        return True
    except:
        return False
