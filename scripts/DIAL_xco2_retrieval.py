#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pn
import xarray as xr

from dialpy.pyOptimalEstimation import pyOptimalEstimation as pyOE
from dialpy.equations.differential_co2_concentration import xco2

priori_names = ["co2_ppm"]
obs_names = ["range_", "delta_sigma_abs", "beta_att_lambda_on", "beta_att_lambda_off", "power_background"]

co2_ppm_model = -np.linspace(0, 1, 320)**2 * np.linspace(0, 1, 320) + np.repeat(400, 320)
co2_ppm_model_sigma = np.repeat(3, 320) + 1 * np.random.rand(320)

forwardKwArgs = {"range_": range_,
                 "delta_sigma_abs": delta_sigma_abs,
                 "beta_att_lambda_on": beta_att_lambda_on,
                 "beta_att_lambda_off": beta_att_lambda_off,
                 "power_background": power_background}

oe = pyOE.optimalEstimation(
    priori_names,  # state variable names
    co2_ppm_model,  # a priori
    co2_ppm_model_sigma,  # a priori uncertainty
    obs_names,  # measurement variable names
    y_obs,  # observations
    S_y[y_vars].loc[y_vars],  # observation uncertainty
    xco2,  # forward Operator
    forwardKwArgs=forwardKwArgs,  # additonal function arguments
)




