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
from dialpy.equations import constants


def forward(X):
    """

    Args:
        X (pandas series): contains CO2 concentration and diff. absorption coefficient

    Returns:
        ratio_of_powers (numpy array): ratio of ON/OFF above/belove powers

    """

    # Extract co2 and diff. abs. coefficient
    n_c, delta_sigma_abs_ = X  # X is pd.Series type
    # ratio of power inverted from the DIAL equation
    ratio_of_powers = np.exp(((1 / (2 * constants.DELTA_RANGE * delta_sigma_abs_)) / n_c)**1)

    return ratio_of_powers


# define names for X and Y
x_vars = ["n_c", "coeffs"]
y_vars = ["Ratio_P"]

# first guess for X
co2_ppm = 400  # (ppm)
delta_sigma_abs = 0.05  # very close to the ground
x_ap = [co2_ppm, delta_sigma_abs]

# covariance matrix for X, uncertainties
x_cov = np.array([[5, 0], [0, .01]])

# covariance matrix for Y, uncertainty
y_cov = np.array([[.1]])

# measured observation of Y, Y_i = [y_below, y_above], delta_sigma_abs, beta_on, beta_off
y_obs = np.array(xco2_beta(np.array([.5, .46]), np.array([1e-4, .5e-4]), np.array([1e-4, 1e-4])))

# create optimal estimation object
oe = pyOE.optimalEstimation(x_vars, x_ap, x_cov, y_vars, y_obs, y_cov, forward)

# run the retrieval
converged = oe.doRetrieval(maxIter=100, maxTime=10000000.0)

# Store results in xarray DataArray
summary = oe.summarize(returnXarray=True)

print(summary.x_op)
print(summary.y_op)
