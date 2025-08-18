import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import typing as t
from typing import Dict, List
from pathlib import Path


def get_summary_stats(df):
    print(df.info())
    print(df[['mpg','displacement','horsepower','acceleration']].describe())
    
def small_op(lst):
    print (f'''List average: {np.average(lst)}''')
    print (f'''List sum: {np.sum(lst)}''')
    print (f'''List standard dev: {np.std(lst)}''')

def year_date_interval_creator():
    today = datetime.today().date()
    one_year_ago = today - timedelta(days=365)
    return today, one_year_ago

def safe_stamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def safe_filename(prefix: str, meta: Dict[str, str]) -> str:
    mid = "_".join([f"{k}-{str(v).replace(' ', '-')[:20]}" for k, v in meta.items()])
    return f"{prefix}_{mid}_{safe_stamp()}.csv"

def validate_df(df: pd.DataFrame, required_cols: List[str], dtypes_map: Dict[str, str]) -> Dict[str, str]:
    msgs = {}
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        msgs['missing_cols'] = f"Missing columns: {missing}"
    for col, dtype in dtypes_map.items():
        if col in df.columns:
            try:
                if dtype == 'datetime64[ns]':
                    pd.to_datetime(df[col])
                elif dtype == 'float':
                    pd.to_numeric(df[col])
            except Exception as e:
                msgs[f'dtype_{col}'] = f"Failed to coerce {col} to {dtype}: {e}"
    na_counts = df.isna().sum().sum()
    msgs['na_total'] = f"Total NA values: {na_counts}"
    return msgs
    
def detect_format(path: t.Union[str, Path]):
    s = str(path).lower()
    if s.endswith('.csv'): return 'csv'
    if s.endswith('.parquet') or s.endswith('.pq') or s.endswith('.parq'): return 'parquet'
    raise ValueError('Unsupported format: ' + s)

def write_df(df: pd.DataFrame, path: t.Union[str, Path]):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    fmt = detect_format(p)
    if fmt == 'csv':
        df.to_csv(p, index=False)
    else:
        try:
            df.to_parquet(p)
        except Exception as e:
            raise RuntimeError('Parquet engine not available. Install pyarrow or fastparquet.') from e
    return p

def read_df(path: t.Union[str, Path]):
    p = Path(path)
    fmt = detect_format(p)
    if fmt == 'csv':
        return pd.read_csv(p, parse_dates=['date']) if 'date' in pd.read_csv(p, nrows=0).columns else pd.read_csv(p)
    else:
        try:
            return pd.read_parquet(p)
        except Exception as e:
            raise RuntimeError('Parquet engine not available. Install pyarrow or fastparquet.') from e
        
def validate_loaded(original, reloaded):
    checks = {
        'shape_equal': original.shape == reloaded.shape,
        'date_is_datetime': pd.api.types.is_datetime64_any_dtype(reloaded['date']) if 'date' in reloaded.columns else False,
        'price_is_numeric': pd.api.types.is_numeric_dtype(reloaded['adjClose']) if 'adjClose' in reloaded.columns else False,
    }
    return checks
