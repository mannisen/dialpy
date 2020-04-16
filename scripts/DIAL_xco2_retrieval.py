#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from dialpy.pyOptimalEstimation import pyOptimalEstimation as pyOE
from dialpy.equations.differential_co2_concentration import xco2_power

# Name of data fields
priori_names = ["co2_ppm"]
obs_names = ["range_", "delta_sigma_abs", "power_on", "power_off", "power_bkg"]

# Prepare priori and its uncertainty
co2_ppm_model = -np.linspace(0, 1, 320)**2 * np.linspace(0, 1, 320) + np.repeat(400, 320)
co2_ppm_model_sigma = np.repeat(3, 320) + 1 * np.random.rand(320)

# Prepare observed variables
range_ = np.arange(0, 9600, 30)
power_off = -np.linspace(0, 1, 320)**2 * np.linspace(0, 1, 320) + 9.9
power_on_hi = -np.linspace(0, 1, 320)**2 * np.linspace(0, 1, 320) + 9.8
power_on = np.hstack((power_off[:100], power_on_hi[100:]))
power_bkg = np.linspace(0, 1, 320) + (np.random.rand(320)+8)
delta_sigma_abs = 1

# Arrange forward model inputs to dictionary
xco2_args = {"range_": range_,
             "delta_sigma_abs": delta_sigma_abs,
             "power_on": power_on,
             "power_off": power_off,
             "power_bkg": power_bkg}

# List observations
obs = [range_, delta_sigma_abs, power_on, power_off, power_bkg]

# Covariance matrix of observations
obs_sigma = np.cov([range_, delta_sigma_abs, power_on, power_off, power_bkg])

# Create optimal estimation object
oe = pyOE.optimalEstimation(
    priori_names,  # state variable names
    co2_ppm_model,  # a priori
    co2_ppm_model_sigma,  # a priori uncertainty
    obs_names,  # measurement variable names
    obs,  # observations
    obs_sigma,  # observation uncertainty
    xco2_power,  # forward Operator
    forwardKwArgs=xco2_args)  # additional function arguments

# Do retrieval
converged = oe.doRetrieval(maxIter=10)




