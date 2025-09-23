import importlib

import pandas as pd
import pymysql

from config import settings


def extract_query(query, params=None) -> pd.DataFrame:
    """Executes SQL query and returns a DataFrame from MySQL.

    :param query: SQL query string.
    :param params: Optional parameters for SQL query.
    :return: Pandas DataFrame containing query results.
    """
    conn = pymysql.connect(
        host=settings.db_url,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
    )
    output = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return output
