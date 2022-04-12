import pandas as pd
import xarray as xr
import os


def input_csv(input_file):
    """Main program to manage plotting, calculation and reading in data"""
    # print(f"using file: {input_file}")
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(e.message, e.args)
        print("ERROR reading in .csv file!")
        # if lat_range is not None:
        #     print("Cannot select latitude range, as none is available in file! Continuing....")
    return df

def input_nc(input_file):
        try:
            with xr.open_dataset(input_file, engine="netcdf4") as ds:
                ds.load()
        except Exception as e:
            print(e.message, e.args)
            print("ERROR reading in .nc file!")
                
        # if lat_range is None:
        #     min_lat = ds.latitude[0].values
        #     max_lat = ds.latitude[-1].values
        # else:
        #     min_lat, max_lat = lat_range
        # print(f"selected latitude range: {min_lat}{degree_sign} to {max_lat}{degree_sign}")
        return ds

def output_data_as_file(df,output_dir,output_file):
        df.to_netcdf(os.path.join(output_dir, output_file))
