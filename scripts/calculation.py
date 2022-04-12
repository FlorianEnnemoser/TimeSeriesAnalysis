import pandas as pd
import numpy as np
import xarray as xr
from scipy import stats


def mean_min_max_temperatures(df):    
    ds_mean = df.mean(["longitude", "latitude"])
    ds_min = df.min(["longitude", "latitude"]).rename("tmin")
    ds_max = df.max(["longitude", "latitude"]).rename("tmax")
      
    return ds_mean, ds_min, ds_max

# needs to accept xarray and do calc then!
def climatology(df):
    """create climatology of given dataframe and return them"""
    ds_clim = df.sel(time=slice("1991-01-01", "2019-12-31")).groupby("time.month").mean()
    monthly_means = df.groupby("time.month")
    return ds_clim, monthly_means


def anomaly(df):
    """create anomalies of given dataframe and return them"""
    clim, monthly_means = climatology(df)
    anom = monthly_means - clim   
    try:
        anom = anom.rename("tanomaly")
    except Exception as e1:
        print(e1,'\n Dataframe consists of more fields - trying to use datavariable renaming...')        
        try: 
            anom = anom.t.rename("tanomaly")
            print("Successfully renamed datavariable!")
        except Exception as e2:
            print(e2)
    return anom

def lin_reg(x, y):
    """Linear Regression with Scipy Stats Library"""
    x = np.array(x, dtype=float)
    result = stats.linregress(x, y)
    y_fitted = result.intercept + result.slope * x
    return y_fitted

def trend_analysis(df):
    """
    Trend analysis of given dataframe using the function lin_reg. 
    Then combining it to a single xarray
    """
    print("start calculating trends...")
    
    
    anomaly_t_r = np.array(anomaly_t, dtype=float)
    
    reg_temp = lin_reg(time_r, temp, int(len(time_r) * sampling_percent))

    print("...finished calculating trends!")
    
    d = {"linregMean": reg_temp, "linregMin": reg_tmin, "linregMax": reg_tmax}
    d_a = {"linregAnom": reg_tanom}
    df_trends1 = pd.DataFrame(data=d, index=time)
    df_trends2 = pd.DataFrame(data=d_a, index=anomaly_t)
    df_trends = pd.concat([df_trends1, df_trends2], axis=1)
    df_trends = df_trends.to_xarray()
    df_trends = df_trends.rename({"index": "time"})
    return df_trends


