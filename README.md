# dialpy

----
2020-05-08

Antti J Manninen

Finnish Meteorological Institute

----
## Minimal working example:

### 0.1) create a virtual environment with pyenv

### 0.2) Install the required dependencies

Written and tested with Python 3.6

|Package|Version|
|-------|-------|
|cftime|1.1.2|
|cycler|0.10.0|
|kiwisolver|1.2.0|
|matplotlib|3.2.1|
|netCDF4|1.5.3|
|numpy|1.18.2|
|pandas|1.0.3|
|pip|19.0.3|
|pyparsing|2.4.7|
|python-dateutil|2.8.1|
|pytz|2019.3|
|scipy|1.4.1|
|setuptools|46.1.3|
|six|1.14.0|
|xarray|0.15.1|

### 1) Clone from github
Open terminal and cd to the folder you want the code package be downloaded to

type:

  `git clone https://github.com/dl-fmi/dialpy`

  `cd dialpy`

  `ls`

and you should see:

  `DIAL_OE_test_co2.png
  DIAL_OE_test_co2_v2.png
  dialpy
  HITRAN_CO2_transition_data.par
  __init__.py
  oe_result.png
  README.md
  scripts
  setup.py
  total_internal_partition_sum.csv`

### 2) Run with simulated inputs
In the current working directory type:

  `python3 -m scripts.DIAL_xco2_retrieval`

Simulated inputs are read, retrieval run, and results are written into a netcdf file and plotted into
*Dial_retrieval.nc* and *DIAL_OR_test_co2.png* files, respectively.

### 3) Run with your own inputs
Open the */scripts/DIAL_xco2_retrieval.py* file and edit the lines 21-33.
Here, you'd call your reader function to get inputs:
 - range
 - delta_sigma_abs
 - beta_att_on (or power_on)
 - beta_att_off (or power_off)
 - co2_ppm
 - temperature
 - pressure

**NOTE**: if you're running the retrieval with power_on and power_off, comment line 32 and uncomment line 34

Script */scripts/DIAL_xco2_retrieval.py* writes the netcdf file into the working directory. Change path and the desired
file name on line 109. Also, the netcdf code requires the data to be given in str and in `YYYYmmdd` format.

For manipulating time values e.g. to unix time */utilities/time_utils.py* has functions for that.

In the current working directory type:

  `python3 -m scripts.DIAL_xco2_retrieval`



