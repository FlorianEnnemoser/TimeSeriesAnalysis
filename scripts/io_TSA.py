import pandas as pd
import xarray as xr


def input_csv(input_file):
    """
    Read in csv file wih pandas. Print Exception if not successful.
    """
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(e.message, e.args)
        print("ERROR reading in .csv file!")
    return df


def input_nc(input_file):
    """
    Read in nc file with xarray. Print Exception if not successful.
    """
    try:
        with xr.open_dataset(input_file, engine="netcdf4") as ds:
            ds.load()
    except Exception as e:
        print(e.message, e.args)
        print("ERROR reading in .nc file!")

    return ds
