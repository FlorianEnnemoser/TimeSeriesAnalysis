"""
Title: Exercise 03
Autor: Florian Ennemoser
Date: 21.01.2022
Course: 411.062 Data Handling in Atmospheric and Climate Physics
"""
import pandas as pd

degree_sign = "\N{DEGREE SIGN}"


def csv_to_xarray(df):
    """
    Convert index to datetime of given dataframe and df to xarray.
    Also drop NaN values.
    """
    df["time"] = pd.to_datetime(df.time)
    df = df.set_index("time")
    df = df.to_xarray()
    df = df.dropna(dim="time")
    return df


def netcdf_latitude_limiting(ds, latmin, latmax):
    """Select latitude min / max range given by user"""
    ds = ds.sel(latitude=slice(latmin, latmax))
    ds = ds.temperature_2_meter.rename("t")

    if ds.attrs["units"] == "K":
        K = 273.15
        ds -= K
        ds.attrs["units"] = f"{degree_sign}C"
        print(
            f"Successfully (automatically) changed temperature scale \
            from K to {degree_sign}C"
        )

    return ds
