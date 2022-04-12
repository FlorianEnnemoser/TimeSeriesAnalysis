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
    default="TAG_Datensatz_19220101_20220101.csv",
    help="input file, has to be inside the >data< folder.",
)
@click.option(
    "--pp",is_flag=True,
    type=click.Choice(["abs", "anom", "absanom"]),
    default="absanom",
    help="option for post processing. Figures display only absolute values (abs), only anomaly (anom) or both (absanom). Default is (absanom)",
)
@click.option(
    "--pp_option",
    type=click.Choice(["abs", "anom", "absanom"]),
    default="absanom",
    help="option for post processing. Figures display only absolute values (abs), only anomaly (anom) or both (absanom). Default is (absanom)",
)
@click.option(
    "--trend",is_flag=True, default=False, help="calculate linear regression for all temperatures."
)
@click.option(
    "--anomaly", is_flag=True,default=False, help="calculate anamoly of given temperature data."
)
@click.option(
    "--output_file",is_flag=True,
    default=False,
    help="select true if an outputfile should be created in the >output< folder",
)
@click.option(
    "--lat_range",
    nargs=2,
    type=float,
    is_flag=True,
    help="select the southern then the northern most latitude, separated by a SPACE. Southern latitudes need to be entered like > -45.2 <. Do not enter degree symbol.",
)
def cli(input_file,lat_range,anomaly,trend,pp,output_file):#, trend,anomaly, pp, lat_range, pp_option, output_file):
    """Simple program that executes the main script. Also prints the elapsed time."""
    t1 = datetime.now()
    print(" Starting script at time: {}".format(t1.strftime('%c')))
    
    loaded_data, csv_flag = input_data_func(input_file)
    preprocessed_df = preprocessing_TSA(loaded_data,csv_flag,lat_range)
    calculated_df = calculation_TSA(preprocessed_df,lat_range,anomaly,trend,csv_flag)
    postprocessing_TSA(calculated_df,pp,trend,anomaly)
    output_data_func(calculated_df,output_file,input_file)
    
    t2 = datetime.now()
    print("Elapsed time: {} (s) \n script finished.".format((t2 - t1).seconds))


def input_data_func(input_file):
    """"""
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

def postprocessing_TSA(calc_df,pp,trend,anomaly):
    if trend:
        postprocessing.create_plotting_with_trends(calc_df,pp,trend,anomaly)
    else:
        postprocessing.create_plotting_without_trends(calc_df,pp,trend,anomaly)
    print("Finished plotting.")
    
def output_data_func(df,output_file,input_file):
    if output_file:
        input_file_split = input_file.split(".")[-1]
        print(input_file_split)
        filename = f'analyzed_TimeSeries_input_{input_file_split}.nc'
        print(f"Saving output to {filename}")
        df.to_netcdf(f'{filename}')
        print("################ DATA SAVED ################\n",df
              ,"\n########################################")
        
    else:
        print("Not saving analyzed data.")


if __name__ == "__main__":
    # f1 = '../TAG_Datensatz_19220101_20220101.csv'
    # f2 = '../temp_data.nc' 
    cli()
    # cli(f1,(40,60),True,True,'anom',False)
    