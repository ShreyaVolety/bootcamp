import sklearn
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

def drop_missing(df, threshold):
    """
    Drop columns with missing values above threshold.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    threshold : float
        Proportion of missing values allowed (0–1).
        
    Returns
    -------
    pd.DataFrame
        Dataframe with columns dropped.
    """
    df_copy = df.copy()
    missing_frac = df_copy.isna().mean()
    cols_to_drop = missing_frac[missing_frac > threshold].index
    return df_copy.drop(columns=cols_to_drop)

def fill_missing_median(df, columns):
    """
    Fill missing values in specified columns (or all numeric columns) with median.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    columns : list, optional
        Columns to apply median fill. If None, applies to all numeric columns.
        
    Returns
    -------
    pd.DataFrame
        Dataframe with missing values filled.
    """
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include="number").columns
    for col in columns:
        median_val = df_copy[col].median()
        df_copy[col] = df_copy[col].fillna(median_val)
    return df_copy


def normalize_data(df, columns):
    """
    Normalize data columns to [0, 1] range using MinMax scaling.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    columns : list, optional
        Columns to normalize. If None, applies to all numeric columns.
        
    Returns
    -------
    pd.DataFrame
        Dataframe with normalized columns.
    """
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include="number").columns
    scaler = MinMaxScaler()
    df_copy[columns] = scaler.fit_transform(df_copy[columns])
    return df_copy