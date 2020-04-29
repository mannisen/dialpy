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
from dialpy.equations.differential_co2_concentration import C_co2_ppm
from dialpy.equations import constants
from scripts import simulated_inputs as sims
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

# Read inputs
range_ = sims.sim_range()
obs_delta_sigma_abs = sims.sim_delta_sigma_abs(range_)
obs_beta_off, obs_beta_on = sims.sim_noisy_beta_att(len(range_), type_='poly1')
N_d, obs_log_ratio_of_powers = xco2_beta(obs_delta_sigma_abs, obs_beta_on, obs_beta_off)
obs_ratio_of_powers = np.exp(obs_log_ratio_of_powers[80:90])

# Initialize
resultsOE = {}


def forward(X):
    """

    Args:
        X (pandas series): contains CO2 concentration, diff. absorption coefficient, temperature, and pressure

    Returns:
        ratio_of_powers (numpy array): ratio of ON/OFF above/belove powers

    """

    # Extract co2 and diff. abs. coefficient
    co2_ppm_, delta_sigma_abs_, T_, P_ = X  # X is pd.Series type

    # invert N_d from co2_ppm, delta_sigma_abs, T_, and P_
    N_d_ = (((1 / constants.LOCHSMIDTS_NUMBER_AIR) * (T_ / 273.15) * (1 / P_) * 1e6) / co2_ppm_)**-1

    # invert ratio of powers (observation) from the DIAL equation
    ratio_of_powers = np.exp((2 * constants.DELTA_RANGE * delta_sigma_abs_) * N_d_)

    return ratio_of_powers


# define names for X and Y
x_vars = ["ratio_of_powers", "delta_sigma_abs", "temperature", "pressure"]
y_vars = ["obs_ratio_of_powers"]

# first guess for X
co2_ppm = np.repeat(400, len(range_[80:90]) - 1)  # (ppm)
T_ = np.repeat(293, len(range_[80:90]) - 1)
P_ = np.repeat(1, len(range_[80:90]) - 1)
delta_sigma_abs = np.repeat(1, len(range_[80:90]) - 1)

for i in range(len(range_[80:90])):

    resultsOE['%s' % (y_vars[0])] = []

    x_ap = pd.Series([co2_ppm[i], obs_delta_sigma_abs[i], T_[i], P_[i]], index=x_vars)

    # covariance matrix for X, uncertainties
    x_cov = np.array([[5, 0, 0, 0], [0, .01, 0, 0], [0, 0, 1, 0], [0, 0, 0, .1]])

    # covariance matrix for Y, uncertainty
    y_cov = np.array([[.001]])

    # measured observation of Y, Y_i = [y_below, y_above], delta_sigma_abs, beta_on, beta_off
    y_obs = pd.Series([obs_ratio_of_powers[i]], index=y_vars)

    # create optimal estimation object
    oe = pyOE.optimalEstimation(x_vars, x_ap, x_cov, y_vars, y_obs, y_cov, forward)

    # run the retrieval
    converged = oe.doRetrieval(maxIter=1000, maxTime=1000000.0)

    if converged:
        # Store results in xarray DataArray
        summary = oe.summarize()
        print(range_[i], summary['x_op'][0], summary['y_op'])

        #resultsOE['%s' % (y_vars[0])].append(summary)

# plt.show()

# store results in xarray Dataset structure
#resultsOE['%s' % (y_vars[0])] = xr.concat(resultsOE['%s' % (y_vars[0])], dim='range_')
