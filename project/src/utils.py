import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import typing as t
from typing import Dict, List
from pathlib import Path
import pandas_market_calendars as mcal


def get_summary_stats(df):
    print(df.info())
    print(df[['mpg','displacement','horsepower','acceleration']].describe())
    
def small_op(lst):
    print (f'''List average: {np.average(lst)}''')
    print (f'''List sum: {np.sum(lst)}''')
    print (f'''List standard dev: {np.std(lst)}''')

def year_date_interval_creator():
    today = datetime.today().date()
    one_year_ago = today - timedelta(days=365*10)
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

def check_missing_dates(dict):
    arr = []
    for df in dict.values():
        df['date'] = pd.to_datetime(df['date'])

    # Get the union of all dates
    all_dates = set()
    for df in dict.values():
        all_dates.update(df['date'])

    # Check which dates are missing in each ticker
    missing_dates = {}
    for ticker, df in dict.items():
        ticker_dates = set(df['date'])
        missing = all_dates - ticker_dates
        if missing:
            missing_dates[ticker] = sorted(missing)

    # Print results
    for ticker, dates in missing_dates.items():
        for d in dates:
            arr.append(d)

    return arr

def read_and_concat(cols,raw_data_path, processed_data_path):

    df = pd.DataFrame()
    ticker_files = {}

    for ticker in cols:
        matching_files = [f for f in os.listdir(raw_data_path) 
                        if f.endswith(".csv") and ticker in f]
        
        if not matching_files:
            raise FileNotFoundError(f"No CSV files found for ticker: {ticker}")
        ticker_files[ticker] = pd.read_csv(raw_data_path+f'/{matching_files[0]}')

    return ticker_files

def get_holidays(start_date, end_date):
    nyse = mcal.get_calendar('NYSE')

    # Get the schedule for this period
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    # Trading days (market open)
    trading_days = schedule.index
    print(trading_days)

    # Optional: see which dates are missing (i.e., holidays)
    all_dates = pd.date_range(start=start_date, end=end_date, freq='B')  # all business days
    holidays = all_dates.difference(trading_days)
    return holidays

def concat_and_save(files, drop_dates):
    final_df = pd.DataFrame()

    for ticker, df in files.items():
        # Flatten any MultiIndex columns
        df.columns = [c if isinstance(c, str) else "_".join(map(str, c)) for c in df.columns]

        if "Date" not in df.columns:
            raise ValueError(f"No 'Date' column found for {ticker}")

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

        df = df[~df["Date"].isin(drop_dates)]

        value_col = [c for c in df.columns if c != "Date"][0]
        df = df[["Date", value_col]].rename(columns={value_col: ticker})

        if final_df.empty:
            final_df = df
        else:
            final_df = pd.merge(final_df, df, on="Date", how="outer")

    final_df = final_df.sort_values("Date").reset_index(drop=True)
    return final_df