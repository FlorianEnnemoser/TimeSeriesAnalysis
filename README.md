# Time Series Analysis
Create a plot of temperature data, even with trends and anomalies by typing
```
plt_tsa --input_file={temperature_data.nc} --absanom --trend --anomaly
```
into the commandline.
## Description
A short program to read in temperature data from ZAMG (in a csv format) or netCDF4 files. 
After reading the data, the time series can be analyzed in several ways.


## Getting Started

### Dependencies
Prerequisits for this script are:

* click
* numpy
* pandas
* matplotlib
* xarray
* netCDF4

They will be installed automatically, see next point.

### Installing
Download the zip file or get the main branch of git.
Then, in the desired folder, unzip the package.
Run the following in the folder:
```
conda create --name mynewenv python
conda activate mynewenv
```
then
```
pip install --editable .
```

### Executing program
Several options are available, they can be called by:
```
plt_tsa --help
```
An input file has to be selected, invoke it by:
```
plt_tsa --inputfule={filename}
```
As an example, here an input file is read in, the absolute, anomalies and trends for temperatures are plotted.
```
plt_tsa --input_file=..\TimeSeriesAnalysis\TAG_Datensatz_19220101_20220101.csv --absanom --trend --anomaly
```
All flags can be added in a random fashion.
Only the --input_file is mandatory.
#### Preprocessing
In the preprocessing step, a latitude range can be defined by:
```
--lat_range x1 x2
```
The values for x1 and x2 can be floats like:
```
--lat_range -10.2 70.65
```

#### Calculation
Concerning the calculation, 2 options are available:
```
--anomaly
```
If given in the command line, the anomaly for the timeframe 1991-01-01 to 2019-12-31 is calculated.

With 
```
--trend
```
the trend for all given temperature time series is calculated.

#### Postprocessing
There are 3 options for postprocessing:
* --abs
* --anom
* --absanom
adding (only one of them) to the command line will plot
the absolute (mean / min / max) temperatures, anomalies or both respectively.

#### Output
With the flag 
```
--output_file
```
an output netCDF4 file (fixed name, depending on the input file) 
is generated, including all temperatures and trends

## Help

Any advise for common problems or issues.
```
plt_tsa --help
```

## Authors
Contributors names

ex. Florian Ennemoser  


## Version History
* 0.1.0
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Data Hubs and Code Inspiration:
* [ZAMG DATA Hub](https://data.hub.zamg.ac.at/)
* [Wegener Center Graz] (https://wegcenter.uni-graz.at/de/)
* [Exercise Preset](https://gitlab.com/flad/exercise_timeseries)
