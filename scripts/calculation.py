import pandas as pd
import numpy as np
import xarray as xr
from scipy import stats


def mean_min_max_temperatures(df):
    K = 273.15
    ds_mean = df.temperature_2_meter.mean(["longitude", "latitude"])
    ds_min = df.temperature_2_meter.min(["longitude", "latitude"])
    ds_max = df.temperature_2_meter.max(["longitude", "latitude"])


# needs to accept xarray and do calc then!
def climatology(df):
    """create climatology of given dataframe and return them"""
    
    ds_clim = df.sel(time=slice("1991-01-01", "2019-12-31")).groupby("time.month").mean()
    
    ds_anom = df.groupby("time.month") - ds_clim
    ds_anom = ds_anom.temperature_2_meter.mean(["longitude", "latitude"]) 
    
    
    climatology = df.groupby(df.index.month).mean()
    climatology.index.name = "month"
    monthly_means = df.groupby([df.index.year, df.index.month]).mean()
    monthly_means.index.names = ["year", "month"]    
    return climatology, monthly_means

def anomaly(df):
    """create anomalies of given dataframe and return them"""
    clim, monthly_means = climatology(df)
    anom = monthly_means - clim
    years = anom.index.get_level_values(0).astype(str)
    months = anom.index.get_level_values(1).astype(str)
    dates = pd.to_datetime(years + "-" + months + "-01")
    anom = anom.set_index(dates)
    return anom

def lin_reg(x, y):
    """Linear Regression with Scipy Stats Library"""
    result = stats.linregress(x, y)
    y_fitted = result.intercept + result.slope * x
    return y_fitted

def trend_analysis(df):
    """
    Trend analysis of given dataframe using the function lin_reg. 
    Then combining it to a single xarray
    """
    print("start calculating trends...")
    
    time_r = np.array(time, dtype=float)
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


