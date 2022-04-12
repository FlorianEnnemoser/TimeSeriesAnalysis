import pandas as pd
import numpy as np
import plotting
import xarray as xr
from scipy import stats



def csv_to_xarray(df):
    """convert index to datetime of given dataframe and df to xarray."""
    df["time"] = pd.to_datetime(df.time)
    df = df.set_index("time")
    df = df.to_xarray()
    df = df.dropna(dim='time')
    return df


def netcdf_latitude_limiting(ds, latmin, latmax):
    """Select latitude min / max range given by user"""
    ds = ds.sel(latitude=slice(latmin, latmax))
    ds = ds.temperature_2_meter.rename("t")
    
    if ds.attrs['units'] =="K":
        K = 273.15
        ds -= K
        ds.attrs['units'] = "°C"
        print("Successfully (automatically) changed temperature scale from K to °C")        
    
    return ds
