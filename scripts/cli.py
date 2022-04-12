import os
import time
import click
import io_TSA
from datetime import datetime
import sys
import preprocessing
import calculation
import plotting
import xarray as xr

# @click.command()
# @click.option(
#     "--input_file",
#     default="TAG_Datensatz_19220101_20220101.csv",
#     help="input file, has to be inside the >data< folder.",
# )
# @click.option(
#     "--pp",is_flag=True,
#     type=click.Choice(["abs", "anom", "absanom"]),
#     default="absanom",
#     help="option for post processing. Figures display only absolute values (abs), only anomaly (anom) or both (absanom). Default is (absanom)",
# )
# @click.option(
#     "--pp_option",
#     type=click.Choice(["abs", "anom", "absanom"]),
#     default="absanom",
#     help="option for post processing. Figures display only absolute values (abs), only anomaly (anom) or both (absanom). Default is (absanom)",
# )
# @click.option(
#     "--trend",is_flag=True, default=False, help="calculate linear regression for all temperatures."
# )
# @click.option(
#     "--anomaly", is_flag=True,default=False, help="calculate anamoly of given temperature data."
# )
# @click.option(
#     "--output_file",is_flag=True,
#     default=False,
#     help="select true if an outputfile should be created in the >output< folder",
# )
# @click.option(
#     "--lat_range",
#     nargs=2,
#     type=float,
#     is_flag=True,
#     help="select the southern then the northern most latitude, separated by a SPACE. Southern latitudes need to be entered like > -45.2 <. Do not enter degree symbol.",
# )
def cli(input_file,lat_range,anomaly,trend,output_file,pp):#, trend,anomaly, pp, lat_range, pp_option, output_file):
    """Simple program that executes the main script. Also prints the elapsed time."""
    t1 = datetime.now()
    print(" Starting script at time: {}".format(t1.strftime('%c')))
    
    loaded_data, csv_flag = input_data_func(input_file)
    preprocessed_df = preprocessing_TSA(loaded_data,csv_flag,lat_range)
    calculated_df = calculation_TSA(preprocessed_df,lat_range,anomaly,trend,csv_flag)
    pp_df = postprocessing_TSA(calculated_df,output_file,pp,trend)
    # output_data_func()
    t2 = datetime.now()
    print("Elapsed time: {} (s) \n script finished.".format((t2 - t1).seconds))


def input_data_func(input_file):
    if input_file.endswith(".csv"):
        df = io_TSA.input_csv(input_file)
        csv_flag = True
    elif input_file.endswith(".nc"):
        df = io_TSA.input_nc(input_file)
        csv_flag = False
    else:
        print("Input data neither .csv nor .nc file! Only available input types are .csv or .nc! \n Exiting...")
        sys.exit()
    return df, csv_flag


def preprocessing_TSA(df,csv_flag,lat_range_flag):
    if csv_flag:
        df = preprocessing.csv_to_xarray(df)
    if lat_range_flag and not csv_flag: ### REMOVE the and not csv_flag >>>>> geht nur wenn lat_flag gesetzt
        latmin, latmax = lat_range_flag
        df = preprocessing.netcdf_latitude_limiting(df, latmin, latmax)
    return df

def calculation_TSA(df,lat_range,anomaly,trend,csv_flag):
    if not csv_flag:
        ds_mean, ds_min, ds_max = calculation.mean_min_max_temperatures(df)    
    else:
        ds_mean = df.t
        ds_max = df.tmax
        ds_min = df.tmin

    if anomaly:
        ds_anom = calculation.anomaly(ds_mean)
        df_merged = xr.merge([ds_mean,ds_min, ds_max,ds_anom])
    else:
        df_merged = xr.merge([ds_mean,ds_min, ds_max])
    
    if trend:
        trend_mean_array = calculation.lin_reg(df_merged)
        
        df_merged['trend_mean'] = ("time",trend_mean_array[0])
        df_merged['trend_min'] = ("time",trend_mean_array[1])
        df_merged['trend_max'] = ("time",trend_mean_array[2])
        
        if anomaly:
            df_merged['trend_anomaly'] = ("time",trend_mean_array[3])
            
    return df_merged

def postprocessing_TSA(calc_df,output_file,pp,trend):
    print(calc_df)
    if trend:
        if pp == "abs":
            plotting.fig_abs_trends_values(calc_df.time,
                                           calc_df.t, calc_df.tmin, calc_df.tmax,
                                           calc_df.trend_mean,calc_df.trend_min,calc_df.trend_max
                                           )
        if pp == "anom":
            plotting.fig_anom_trends_values(calc_df.time,
                                           calc_df.tanomaly,calc_df.trend_anomaly)
        if pp == "absanom":
            plotting.fig_abs_anom_trends_values(
                calc_df.time, 
                calc_df.t, calc_df.tmin, calc_df.tmax,
                calc_df.tanomaly,
                calc_df.trend_mean,calc_df.trend_min,calc_df.trend_max,calc_df.trend_anomaly
            )
        plotting.save_figure(f"{output_dir}/output_plotting_trends_{mode}.png")
    else:

        
    

    # else:
    #     print("plotting and not adding Trend")
    #     if mode == "abs":
    #         plotting.fig_abs_values(time, temp, tmin, tmax)
    #     if mode == "anom":
    #         plotting.fig_anom_values(anomaly_t, anomaly)
    #     if mode == "absanom":
    #         plotting.fig_abs_anom_values(time, temp, tmin, tmax, anomaly_t, anomaly)
    #     plotting.save_figure(f"{output_dir}/output_plotting_{mode}.png")


        
    
    return

    
def output_data_func():
    return
#io -i
#preprocessing
#calculation
#postprocessing
#io -o

    


if __name__ == "__main__":
    f1 = '../TAG_Datensatz_19220101_20220101.csv'
    f2 = '../temp_data.nc' 
    
    cli(f2,(40,60),True,True,True,'absanom')
    