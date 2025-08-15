import pandas as pd

def get_summary_stats(df):
    print(df.info())
    print(df[['mpg','displacement','horsepower','acceleration']].describe())
    