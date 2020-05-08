#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
from dialpy.pyOptimalEstimation import pyOptimalEstimation as pyOE
from dialpy.equations.differential_co2_concentration import xco2_beta
from dialpy.equations.differential_co2_concentration import xco2_power
from dialpy.equations import constants
from scripts import simulated_inputs as sims
import matplotlib.pyplot as plt
from dialpy.utilities.dl_var_atts import dl_var_atts as vatts

# Read inputs
range_ = sims.sim_range()
delta_sigma_abs = sims.sim_delta_sigma_abs(range_)
obs_beta_off, obs_beta_on = sims.sim_noisy_beta_att(len(range_), type_='poly2')

# first guess for X - can be from a model, sounding, in-situ observation...
co2_ppm = np.repeat(400, len(range_) - 1)  # (ppm)
T_ = np.repeat(293, len(range_) - 1)  # (K)
P_ = np.repeat(1, len(range_) - 1)  # (atm)

# if you have calibrated (or wish to run retrieval with uncalibrated) attenuated beta, use:
N_d, log_ratio_of_powers = xco2_beta(delta_sigma_abs, obs_beta_on, obs_beta_off)
# if you wish to run the retrieval with power (integrated Doppler spectra), use:
# N_d, log_ratio_of_powers = xco2_power(delta_sigma_abs, obs_beta_on, obs_beta_off)

# Initialize
resultsOE = {}
res = np.empty([len(co2_ppm), 3])  # range, co2_ppm, T_optimal, P_optimal
res[:] = np.nan
res[:, 0] = range_[:-1]


# Define forward model
def forward(X):
    """Number density inverted from Eq. (7) in http://dx.doi.org/10.1364/AO.52.002994

    Args:
        X (pandas series): contains CO2 concentration, diff. absorption coefficient, temperature, and pressure

    Returns:
        N_d (numpy array): number density of trace gas (# m-3)

    """

    # Extract co2 and diff. abs. coefficient
    co2_ppm_, T_, P_ = X  # X is pd.Series type

    # invert N_d from co2_ppm with given delta_sigma_abs, T_, and P_
    N_L_ = constants.LOCHSMIDTS_NUMBER_AIR

    return (co2_ppm_ * N_L_ * 273.15 * P_) / (T_ * 1e6) / 1e22


# define names for x and y variables
x_vars = ["co2_ppm", "temperature", "pressure"]
y_vars = ["N_d"]

# for i in range(len(time_)):  # loop over time stamps

# Loop over range gates - this should be done a profile at a time to speed up. pyOEcore.py gives errors though!
for i in range(len(range_)-1):

    x_ap = [co2_ppm[i], T_[i], P_[i]]

    # covariance matrix for X, uncertainties
    x_cov = np.array([[5, 0, 0], [0, 1, 0], [0, 0, .1]])  # units: [[(ppm), 0, 0], [0, (K), 0]. [0, 0, (atm)]]

    # covariance matrix for Y, uncertainty
    y_cov = np.array([1])  # units: m-2 / 1e21  --> scaled!

    # measured observation of Y, Y_i = [y_below, y_above], delta_sigma_abs, beta_on, beta_off
    y_obs = np.array(N_d[i]/1e21)  # scale to within same ball park (order of magnitude) as with other inputs

    # create optimal estimation object
    oe = pyOE.optimalEstimation(x_vars, x_ap, x_cov, y_vars, y_obs, y_cov, forward)

    # run the retrieval
    converged = oe.doRetrieval(maxIter=100)  # check options within, max time can be set as well

    if converged:
        # Store results in xarray DataArray
        summary = oe.summarize()
        print(range_[i], summary['x_op'][0], summary['y_op'][0])

        res[i, 1] = float(summary['x_op'][0])
        res[i, 2] = float(summary['y_op'][0]*1e22)

temperature_out = vatts("temperature", data=T_, dim_size=len(T_))
pressure_out = vatts("temperature", data=P_, dim_size=len(P_))
co2_ppm_priori_out = vatts("carbon_dioxide_concentration_priori", data=co2_ppm, dim_size=len(co2_ppm))

data_out = list()

fig = plt.figure()
ax0 = plt.subplot2grid((1, 3), (0, 0), rowspan=1, colspan=1)
p01 = ax0.plot(obs_beta_off*1e6, range_, label='$\\beta_{att}$ OFF')
p02 = ax0.plot(obs_beta_on*1e6, range_, label='$\\beta_{att}$ ON')
ax0.legend(loc='upper right')
ax0.set_xlabel("(Mm-1 sr-1)")
ax0.set_ylabel("range (km)")
ax0.grid()

ax1 = plt.subplot2grid((1, 3), (0, 1), rowspan=1, colspan=1)
p11 = ax1.plot(N_d, range_[:-1], label='Observed N_d')
p12 = ax1.plot(res[:, 2], range_[:-1], label='Optimal N_d')
ax1.legend(loc='upper right')
ax1.set_xlabel("(# m-3)")
ax1.grid()

ax2 = plt.subplot2grid((1, 3), (0, 2), rowspan=1, colspan=1)
p21 = ax2.plot(res[:, 1], range_[:-1], label='Retrieved CO2')
p22 = ax2.plot(co2_ppm, range_[:-1], label='Initial guess of CO2')
ax2.legend(loc='upper right')
ax2.set_xlabel("(ppm)")
ax2.grid()

fig.tight_layout()
plt.savefig("DIAL_OE_test_co2_v2.png", facecolor='w', edgecolor='w',
            format="png", bbox_inches="tight", pad_inches=0.1)
plt.close()
