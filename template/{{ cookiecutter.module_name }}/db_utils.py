"""Database query utilities for MySQL, AWS Athena, and Google BigQuery.

This module provides small helpers to execute SQL queries against different
backends and to normalize attribute tables. It aims to keep interfaces simple
and return pandas-compatible results where possible.

Notes:
    - External dependencies include pymysql, pyathena, boto3,
      google-cloud-bigquery, and pandas.
    - Credentials and connection details are read from config.settings.
"""

import boto3
from google.cloud import bigquery
from google.oauth2 import service_account
import numpy as np
import pandas as pd
from pyathena import connect
import pymysql

from config import settings


def extract_query(query, params=None) -> pd.DataFrame:
    """Execute a SQL query against MySQL and return a DataFrame.

    Establishes a direct connection using credentials from `settings` and
    executes the provided SQL. The connection is closed after the read.

    Args:
        query (str): The SQL query string.
        params (dict | list | tuple | None): Optional parameters passed to the
            SQL engine. Use DB-API parameter styles supported by pymysql.

    Returns:
        pandas.DataFrame: Query results as a DataFrame.

    Raises:
        pymysql.MySQLError: If the connection or query execution fails.

    Examples:
        >>> df = extract_query("SELECT * FROM users WHERE id=%s", params=[1])
        >>> len(df) >= 0
        True
    """
    # Open a new MySQL connection using configured credentials.
    conn = pymysql.connect(
        host=settings.db_url,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
    )

    # Execute the query and load results into a DataFrame.
    output = pd.read_sql_query(query, conn, params=params)

    # Ensure the connection is closed before returning.
    conn.close()
    return output


def merge_values(attributes_df: pd.DataFrame) -> pd.DataFrame:
    """Merge non-null attribute value columns into a single `value` column.

    Searches for columns whose names contain the `'v_'` pattern (case
    insensitive), backfills across those columns row-wise, and keeps only the
    first non-null entry as `value`. The original value columns are dropped.

    Args:
        attributes_df (pandas.DataFrame): DataFrame that may contain multiple
            attribute value columns (e.g., `v_text, ``v_int`).

    Returns:
        pandas.DataFrame: The same DataFrame reference with a single
        `value` column replacing the original value-specific columns.

    Notes:
        This function mutates `attributes_df` in place (drops columns and
        assigns a new `value` column) and also returns it for convenience.
    """
    # Identify columns that match our value naming pattern.
    value_columns = [col for col in attributes_df.columns if "v_" in col.lower()]

    # If value-like columns exist, backfill row-wise to capture the first value.
    if value_columns:
        attributes_df["value"] = attributes_df[value_columns].bfill(axis=1).iloc[:, 0]
        attributes_df = attributes_df.drop(value_columns, axis=1)

    return attributes_df


def query_athena(
    query: str, params=None, profile_name=settings.db_s3_username
) -> pd.DataFrame:
    """Execute a SQL query in AWS Athena and return a DataFrame.

    Accepts optional parameters for substitution. If `params` is a single
    list-like intended for an `IN` clause, the function rewrites the query's
    `IN ?` placeholder to the appropriate number of `%s` placeholders.

    Args:
        query (str): SQL query string. Use `?` as a placeholder that will be
            mapped to DB-API `%s` when `params` are provided.
        params (list | dict | None): Parameters to substitute into the query.
            If `params` is a list containing exactly one list-like (list,
            `pandas.Series, or ``numpy.ndarray`), it is treated as values
            for an `IN` clause and expanded accordingly.
        profile_name (str): Name of the AWS credentials profile to use.

    Returns:
        pandas.DataFrame: Query results as a DataFrame.

    Raises:
        pyathena.error.OperationalError: On Athena execution failures.
        boto3.exceptions.Boto3Error: On AWS session or credential issues.
        ValueError: If placeholders and parameters are mismatched.

    Examples:
        Basic usage:
            >>> df = query_athena("SELECT 1 AS x")
        IN-clause expansion:
            >>> ids = [1, 2, 3]
            >>> df = query_athena("SELECT * FROM t WHERE id IN ?", params=[ids])
    """
    # Initialize a boto3 session for the specified profile/region.
    session = boto3.Session(profile_name=profile_name, region_name="eu-west-1")

    # Create an Athena connection using the configured S3 staging directory.
    conn = connect(
        s3_staging_dir=settings.db_s3_bucket,
        region_name="eu-west-1",
        work_group="tableau-production",
        boto3_session=session,
    )

    # Handle the special case: params is a single list-like for an IN clause.
    if (
        isinstance(params, list)
        and len(params) == 1
        and isinstance(params[0], list | pd.Series | np.ndarray)
    ):
        values = list(params[0])
        # Build a comma-separated list of '%s' placeholders.
        placeholders = ",".join(["%s"] * len(values))
        # Replace a single 'IN ?' with the expanded placeholders.
        query = query.replace("IN ?", f"IN ({placeholders})")
        params = values

    # Execute the query and return results as a DataFrame.
    return pd.read_sql(query, conn, params=params)


def query_bigquery(query: str):
    """Execute a SQL query against Google BigQuery.

    Creates explicit service account credentials from the path in
    `settings.db_bq_cred` and runs the query in the project
    `'production-247608'`.

    Args:
        query (str): Standard SQL query string.

    Returns:
        google.cloud.bigquery.table.RowIterator: An iterator over result rows.
        Use `list(...)` or iterate to consume results, or convert to a
        DataFrame via `client.query(...).result().to_dataframe()` if needed.

    Raises:
        google.auth.exceptions.GoogleAuthError: If credentials are invalid.
        google.api_core.GoogleAPIError: On BigQuery client or execution errors.

    Examples:
        >>> rows = query_bigquery("SELECT 1 AS x")
        >>> isinstance(rows.total_rows, int)
        True
    """
    # Load service account credentials from the configured JSON key path.
    key_path = settings.db_bq_creds
    print(key_path)
    credentials = service_account.Credentials.from_service_account_file(key_path)

    # Initialize a BigQuery client with explicit project and credentials.
    client = bigquery.Client(project="production-247608", credentials=credentials)

    # Submit the query job and block until completion, returning an iterator.
    return client.query(query).result().to_dataframe()
