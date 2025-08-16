import pandas as pd
import numpy as np

def get_summary_stats(df):
    print(df.info())
    print(df[['mpg','displacement','horsepower','acceleration']].describe())
    
def small_op(lst):
    print (f'''List average: {np.average(lst)}''')
    print (f'''List sum: {np.sum(lst)}''')
    print (f'''List standard dev: {np.std(lst)}''')