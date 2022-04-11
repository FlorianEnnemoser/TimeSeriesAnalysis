import pandas as pd
import numpy as np
import plotting
import xarray as xr
from scipy import stats



def df_add_calculation_results(df):
    analysis = climate(df)
    anomaly = analysis[2].t.values
    anomaly_t = analysis[2].t.index.values
    d_anom = {"anomaly": anomaly}
    df_analysis = pd.DataFrame(data=d_anom, index=anomaly_t)
    df_tot = pd.concat([df, df_analysis], axis=1)
    df_tot = df_tot.to_xarray()
    df_tot = df_tot.rename({"index": "time"})
    
    