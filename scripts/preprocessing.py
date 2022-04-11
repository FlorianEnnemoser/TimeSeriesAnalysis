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
    return df


def netcdf_latitude_limiting(ds, latmin, latmax):
    """Select latitude min / max range given by user"""
    ds = ds.sel(latitude=slice(latmin, latmax))
    # ds_edit = xr.merge(
    #     [
    #         ds_mean.rename("t"),
    #         ds_min.rename("tmin"),
    #         ds_max.rename("tmax"),
    #         ds_anom.rename("anomaly"),
    #     ]
    # )
    return ds
