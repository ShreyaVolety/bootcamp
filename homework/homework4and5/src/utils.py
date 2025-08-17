import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

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
    