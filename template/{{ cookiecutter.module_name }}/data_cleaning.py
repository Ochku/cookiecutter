"""Data cleaning utilities and preprocessing functions."""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import re

from config import settings


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names by removing special characters and standardizing format.

    Args:
        df: DataFrame to clean

    Returns:
        DataFrame with cleaned column names
    """
    df_clean = df.copy()

    # Convert to lowercase and replace spaces/special chars with underscores
    df_clean.columns = df_clean.columns.str.lower()
    df_clean.columns = df_clean.columns.str.replace(r"[^a-z0-9_]", "_", regex=True)
    df_clean.columns = df_clean.columns.str.replace(r"_+", "_", regex=True)
    df_clean.columns = df_clean.columns.str.strip("_")

    return df_clean


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = "drop",
    fill_value: Any = None,
    threshold: float = 0.5,
) -> pd.DataFrame:
    """Handle missing values in DataFrame.

    Args:
        df: DataFrame to clean
        strategy: Strategy to use ('drop', 'fill', 'interpolate')
        fill_value: Value to fill missing data with (for 'fill' strategy)
        threshold: Threshold for dropping columns/rows (for 'drop' strategy)

    Returns:
        DataFrame with missing values handled
    """
    df_clean = df.copy()

    if strategy == "drop":
        # Drop columns with more than threshold missing values
        df_clean = df_clean.dropna(axis=1, thresh=int(len(df_clean) * (1 - threshold)))
        # Drop rows with any remaining missing values
        df_clean = df_clean.dropna()

    elif strategy == "fill":
        if fill_value is not None:
            df_clean = df_clean.fillna(fill_value)
        else:
            # Fill numeric columns with median, categorical with mode
            for col in df_clean.columns:
                if df_clean[col].dtype in ["int64", "float64"]:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                else:
                    df_clean[col].fillna(
                        (
                            df_clean[col].mode()[0]
                            if not df_clean[col].mode().empty
                            else "Unknown"
                        ),
                        inplace=True,
                    )

    elif strategy == "interpolate":
        df_clean = df_clean.interpolate(method="linear")

    return df_clean


def remove_duplicates(
    df: pd.DataFrame, subset: Optional[List[str]] = None
) -> pd.DataFrame:
    """Remove duplicate rows from DataFrame.

    Args:
        df: DataFrame to clean
        subset: List of columns to consider for duplicates

    Returns:
        DataFrame with duplicates removed
    """
    return df.drop_duplicates(subset=subset, keep="first")


def standardize_text(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Standardize text in specified columns.

    Args:
        df: DataFrame to clean
        columns: List of column names to standardize

    Returns:
        DataFrame with standardized text
    """
    df_clean = df.copy()

    for col in columns:
        if col in df_clean.columns:
            # Convert to string, strip whitespace, convert to lowercase
            df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()

    return df_clean


def detect_outliers_iqr(
    df: pd.DataFrame, columns: List[str], factor: float = 1.5
) -> pd.DataFrame:
    """Detect outliers using IQR method.

    Args:
        df: DataFrame to analyze
        columns: List of numeric columns to check
        factor: IQR factor for outlier detection

    Returns:
        DataFrame with outlier flags
    """
    df_clean = df.copy()

    for col in columns:
        if col in df_clean.columns and df_clean[col].dtype in ["int64", "float64"]:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - factor * IQR
            upper_bound = Q3 + factor * IQR

            df_clean[f"{col}_outlier"] = (df_clean[col] < lower_bound) | (
                df_clean[col] > upper_bound
            )

    return df_clean


def convert_data_types(df: pd.DataFrame, type_mapping: Dict[str, str]) -> pd.DataFrame:
    """Convert data types of specified columns.

    Args:
        df: DataFrame to convert
        type_mapping: Dictionary mapping column names to target types

    Returns:
        DataFrame with converted data types
    """
    df_clean = df.copy()

    for col, dtype in type_mapping.items():
        if col in df_clean.columns:
            try:
                if dtype == "datetime":
                    df_clean[col] = pd.to_datetime(df_clean[col])
                elif dtype == "category":
                    df_clean[col] = df_clean[col].astype("category")
                else:
                    df_clean[col] = df_clean[col].astype(dtype)
            except Exception as e:
                print(f"Warning: Could not convert column '{col}' to {dtype}: {e}")

    return df_clean


def clean_data_pipeline(
    df: pd.DataFrame,
    clean_columns: bool = True,
    handle_missing: bool = True,
    remove_dups: bool = True,
    text_columns: Optional[List[str]] = None,
    outlier_columns: Optional[List[str]] = None,
    type_mapping: Optional[Dict[str, str]] = None,
) -> pd.DataFrame:
    """Complete data cleaning pipeline.

    Args:
        df: DataFrame to clean
        clean_columns: Whether to clean column names
        handle_missing: Whether to handle missing values
        remove_dups: Whether to remove duplicates
        text_columns: List of text columns to standardize
        outlier_columns: List of columns to check for outliers
        type_mapping: Dictionary for data type conversions

    Returns:
        Cleaned DataFrame
    """
    df_clean = df.copy()

    if clean_columns:
        df_clean = clean_column_names(df_clean)

    if handle_missing:
        df_clean = handle_missing_values(df_clean)

    if remove_dups:
        df_clean = remove_duplicates(df_clean)

    if text_columns:
        df_clean = standardize_text(df_clean, text_columns)

    if outlier_columns:
        df_clean = detect_outliers_iqr(df_clean, outlier_columns)

    if type_mapping:
        df_clean = convert_data_types(df_clean, type_mapping)

    return df_clean


# Example usage
if __name__ == "__main__":
    # Create sample data with issues
    sample_data = pd.DataFrame(
        {
            "Name": [
                "John Doe",
                "Jane Smith",
                "Bob Johnson",
                "Alice Brown",
                "John Doe",
            ],
            "Age": [25, 30, None, 35, 25],
            "Salary": [50000, 60000, 70000, 80000, 50000],
            "Department": ["IT", "HR", "IT", "Finance", "IT"],
            "Email": [
                "john@email.com",
                "jane@email.com",
                "bob@email.com",
                "alice@email.com",
                "john@email.com",
            ],
        }
    )

    print("Original data:")
    print(sample_data)
    print("\nData info:")
    print(sample_data.info())

    # Clean the data
    cleaned_data = clean_data_pipeline(
        sample_data,
        text_columns=["Name", "Department"],
        outlier_columns=["Age", "Salary"],
        type_mapping={"Age": "float64", "Salary": "int64"},
    )

    print("\nCleaned data:")
    print(cleaned_data)
    print("\nCleaned data info:")
    print(cleaned_data.info())
