import pandas as pd
import numpy as np
import scipy
from scipy import stats

def detect_outliers(series: pd.Series, method: str = "zscore", threshold: float = 3.0) -> pd.Series:
    
    if method == "zscore":
        z_scores = np.abs(stats.zscore(series.dropna()))
        mask = pd.Series(False, index=series.index)
        mask[series.dropna().index] = z_scores > threshold
        return mask

    elif method == "iqr":
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        return (series < lower) | (series > upper)

    else:
        raise ValueError("method must be 'zscore' or 'iqr'")
