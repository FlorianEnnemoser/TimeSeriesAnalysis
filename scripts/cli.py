"""
Title: Exercise 03
Autor: Florian Ennemoser
Date: 21.01.2022
Course: 411.062 Data Handling in Atmospheric and Climate Physics
"""
import click
import io_TSA
from datetime import datetime
import sys
import preprocessing
import postprocessing
import calculation
import xarray as xr


@click.command()
@click.option(
    "--input_file",
    required=True,
    help="input file where data is taken from. Required!",
)
@click.option(
    "--lat_range",
    nargs=2,
    type=float,
    help="select the southern then the northern most latitude,\
        separated by a SPACE. Southern latitudes need to be \
        entered like > -45.2 <. Do not enter degree symbol.\
        (inactive per default)",
)
@click.option(
    "--abs",
    "pp",
    flag_value="abs",
    default=True,
    help="Postprocessing Flag - Plot only \
        absolute temperature values. (default value)",
)
@click.option(
    "--anom",
    "pp",
    flag_value="anom",
    help="Postprocessing Flag - Plot only \
        anomaly temperature values.",
)
@click.option(
    "--absanom",
    "pp",
    flag_value="absanom",
    help="Postprocessing Flag - Plot absolute\
        and anomaly temperature values.",
)
@click.option(
    "--trend",
    is_flag=True,
    default=False,
    help="flag to calculate linear regression \
        for all given temperature values. (default is false)",
)
@click.option(
    "--anomaly",
    is_flag=True,
    default=False,
    help="flag to calculate anamoly \
        of given temperature data. (default is false)",
)
@click.option(
    "--output_file",
    is_flag=True,
    default=False,
    help="flag to create an outputfile \
        of analyzed data (inactive per default)",
)
def tsa(input_file, lat_range, anomaly, trend, pp, output_file):
    """
    A script for analyzing a time series. Input data is loaded, preprocessed,
    calculations are done, and finally postprocessed.
    Several options are available, see --help.
    """

    t1 = datetime.now()
    print(" Starting script at time: {}".format(t1.strftime("%c")))

    loaded_data, csv_flag = input_data_func(input_file)
    preprocessed_df = preprocessing_TSA(loaded_data, csv_flag, lat_range)
    calculated_df = calculation_TSA(
        preprocessed_df, lat_range, anomaly, trend, csv_flag
    )
    postprocessing_TSA(calculated_df, pp, trend, anomaly)
    output_data_func(calculated_df, output_file, input_file)

    t2 = datetime.now()
    print("Elapsed time: {} (s) \n script finished.".format((t2 - t1).seconds))


def input_data_func(input_file):
    """
    Load in given data. Sets csv_flag accordingly
    to file ending. Exists script if incorrect data is given.
    """
    if input_file.endswith(".csv"):
        df = io_TSA.input_csv(input_file)
        csv_flag = True
    elif input_file.endswith(".nc"):
        df = io_TSA.input_nc(input_file)
        csv_flag = False
    else:
        print(
            "Input data neither .csv nor .nc file! \
            Only available input types are .csv or .nc! \n Exiting..."
        )
        sys.exit()
    return df, csv_flag


def preprocessing_TSA(df, csv_flag, lat_range_flag):
    """
    Preprocessing of given data.
    Transforms non .nc files to xarray dataset. Also limits latitude range.
    """
    if csv_flag:
        df = preprocessing.csv_to_xarray(df)
    if lat_range_flag and not csv_flag:
        latmin, latmax = lat_range_flag
        df = preprocessing.netcdf_latitude_limiting(df, latmin, latmax)
    return df


def calculation_TSA(df, lat_range, anomaly, trend, csv_flag):
    """
    Calculation of data, depending on flags for anomaly and trend.
    In the end, a merged xarray dataset is returned,
    containing all user specified temperatures.
    """
    if not csv_flag:
        ds_mean, ds_min, ds_max = calculation.mean_min_max_temperatures(df)
    else:
        ds_mean = df.t
        ds_max = df.tmax
        ds_min = df.tmin

    if anomaly:
        ds_anom = calculation.anomaly(ds_mean)
        df_merged = xr.merge([ds_mean, ds_min, ds_max, ds_anom])
    else:
        df_merged = xr.merge([ds_mean, ds_min, ds_max])

    if trend:
        trend_mean_array = calculation.lin_reg(df_merged)

        df_merged["trend_mean"] = ("time", trend_mean_array[0])
        df_merged["trend_min"] = ("time", trend_mean_array[1])
        df_merged["trend_max"] = ("time", trend_mean_array[2])

        if anomaly:
            df_merged["trend_anomaly"] = ("time", trend_mean_array[3])

    return df_merged


def postprocessing_TSA(calc_df, pp, trend, anomaly):
    """
    Postprocessing of data.
    Creates plots depending on trend and anomaly flag.
    """
    print("Start Postprocessing...")
    if trend:
        postprocessing.create_plotting_with_trends(calc_df, pp, anomaly)
    else:
        postprocessing.create_plotting_without_trends(calc_df, pp, anomaly)
    print("...Finished Postprocessing.")


def output_data_func(df, output_file, input_file):
    """
    The given dataset is saved as a netCDF4 file.
    The name is fixed as of the current version.
    """
    if output_file:
        input_file_split = input_file.split(".")[-1]
        filename = f"analyzed_TimeSeries_input_{input_file_split}.nc"
        print(f"Saving output to {filename}")
        df.to_netcdf(f"{filename}")
        print(
            "################ DATA SAVED ################\n",
            df,
            "\n########################################",
        )

    else:
        print("Not saving analyzed data.")


if __name__ == "__main__":
    tsa()
