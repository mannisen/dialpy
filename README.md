# dialpy

Not published, under development.

Go to terminal

git clone...

cd ../dialpy

ll

-you should see:
DIAL_OE_test_co2.png  DIAL_OE_test_co2_v2.png  dialpy  HITRAN_CO2_transition_data.par  __init__.py
oe_result.png  README.md  scripts  setup.py  total_internal_partition_sum.csv

Then, in the current working directory the DIAL retrieval code can be run by typing:
python3 -m scripts.DIAL_xco2_retrieval

Simulated inputs are read, retrieval run, and results are written into a netcdf file in folder "".
Results are plotted into the same folder into file "".__init__

If you wish to run the code with your input, open the DIAL_xco2_retrieval.py file and edit the lines 21-33,
where you'd call reader function to get range, delta_sigma_abs, beta_att_on (or power_on), beta_att_off (or power_off),
co2_ppm, temperature, pressure.

NOTE: if you're running the retrieval with power_on and power_off, comment line 32 and uncomment line 34

