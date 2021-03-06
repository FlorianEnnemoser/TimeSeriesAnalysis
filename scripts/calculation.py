"""
Title: Exercise 03
Autor: Florian Ennemoser
Date: 21.01.2022
Course: 411.062 Data Handling in Atmospheric and Climate Physics
"""
import numpy as np


def mean_min_max_temperatures(df):
    """
    Adds mean, min. and max. temperature (over latitude and longitude)
    and returns those as data-arrays
    """
    try:
        ds_mean = df.mean(["longitude", "latitude"])
        ds_min = df.min(["longitude", "latitude"]).rename("tmin")
        ds_max = df.max(["longitude", "latitude"]).rename("tmax")
    except Exception as e0:
        print("ERROR at calculation - trying alternative renaming.\n Error: ", e0)
        ds_mean = df.temperature_2_meter.mean(["longitude", "latitude"]).rename("t")
        ds_min = df.temperature_2_meter.min(["longitude", "latitude"]).rename("tmin")
        ds_max = df.temperature_2_meter.max(["longitude", "latitude"]).rename("tmax")
    return ds_mean, ds_min, ds_max


def climatology(df):
    """create climatology of given dataframe and return them"""
    ds_clim = (
        df.sel(time=slice("1991-01-01", "2019-12-31")).groupby("time.month").mean()
    )
    monthly_means = df.groupby("time.month")
    return ds_clim, monthly_means


def anomaly(df):
    """create anomalies of given dataframe and return them"""
    clim, monthly_means = climatology(df)
    anom = monthly_means - clim
    try:
        anom = anom.rename("tanomaly")
    except Exception as e1:
        print(
            e1,
            "\n Dataframe consists of more fields - trying to use datavariable renaming...",
        )
        try:
            anom = anom.t.rename("tanomaly")
            print("Successfully renamed datavariable!")
        except Exception as e2:
            print(e2, "ERROR ")
    return anom


def lin_reg(df):
    """Linear Regression with Numpy Polyfit Library"""
    x = np.array(df.time, dtype=float)
    y = df.to_array()
    k_arr, d_arr = np.polyfit(x, y.T, 1)

    y_fitted = np.empty_like(y)
    for i, k in enumerate(k_arr):
        y_fitted[i, :] = k * x + d_arr[i]

    return y_fitted
