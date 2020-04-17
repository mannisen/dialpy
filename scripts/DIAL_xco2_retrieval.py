#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from dialpy.pyOptimalEstimation import pyOptimalEstimation as pyOE
from dialpy.equations.differential_co2_concentration import xco2_beta
from scipy.optimize import curve_fit

# Name of data fields
x_vars = ["delta_sigma_abs", "beta_att_lambda_on", "beta_att_lambda_off"]
y_vars = ["co2_ppm"]

# variables
range_ = np.array(np.linspace(0, 10, num=400))
coeff = np.array(np.random.uniform(.999, 1.001, (400, )))
delta_sigma_abs = coeff * 1
c = -np.linspace(0, 1, num=400)**2 * np.linspace(0, 1, num=400) + 1
c_abs = np.hstack((c[:80], c[80:]-.1))
obs_beta_att_lambda_on = np.random.uniform(.8e-7, 1.2e-7, (400, )) * c_abs
obs_beta_att_lambda_off = np.random.uniform(.8e-7, 1.2e-7, (400, )) * c

# Arrange forward model inputs to dictionary
xco2_args = {"range_": range_,
             "delta_sigma_abs": delta_sigma_abs,
             "beta_att_lambda_on": beta_att_lambda_on,
             "beta_att_lambda_off": beta_att_lambda_off}


# # Prepare priori and its uncertainty
co2_ppm = xco2_beta(delta_sigma_abs, beta_att_lambda_on, beta_att_lambda_off, power_bkg)
co2_ppm_sigma = np.var(co2_ppm)

# Covariance matrix of observations
obs_sigma = np.cov(obs)

# Create optimal estimation object
oe = pyOE.optimalEstimation(
    priori_names,  # state variable names
    co2_ppm,  # a priori
    co2_ppm_sigma,  # a priori uncertainty
    obs_names,  # measurement variable names
    obs,  # observations
    obs_sigma,  # observation uncertainty
    xco2_power,  # forward Operator
    forwardKwArgs=xco2_args)  # additional function arguments

# Do retrieval
converged = oe.doRetrieval(maxIter=10)




