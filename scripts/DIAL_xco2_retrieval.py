#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from dialpy.pyOptimalEstimation import pyOptimalEstimation as pyOE
from dialpy.equations.differential_co2_concentration import xco2_beta
from dialpy.equations import absroption_corss_section as acs
from dialpy.utilities import general_utils as gu
from scipy.optimize import curve_fit

# Name of data fields
x_vars = ["delta_sigma_abs", "beta_att_lambda_on", "beta_att_lambda_off"]
y_vars = ["co2_ppm"]

# variables
# range
range_ = np.array(np.linspace(0, 10, num=400))

# model temperature
T_ = -range_ * 5 + 5 + 273.15  # (K)
# model pressure
P_ = (-range_ * .08 + 1) * 101325  # Pa

# generate simulated att beta profiles
b = -range_**2 + -range_ + 0
b_n = gu.renormalize(b, [b.min(), b.max()], [0, 1])
c = np.empty(400, )
for i in range(len(range_)):
    dice = np.random.rand()
    if dice > .5:
        c[i] = b_n[i] + np.random.uniform(.1, .2)
    else:
        c[i] = b_n[i] - np.random.uniform(.1, .2)
obs_beta_off = gu.renormalize(c, [c.min(), c.max()], [0, .7])
aaa = np.array([0, .075 ,.5, .925, 1])
obs_beta_on = np.hstack((obs_beta_off[:80], obs_beta_off[80:85]-aaa*.05, obs_beta_off[85:]-.05))

# Arrange forward model inputs to dictionary
xco2_args = {"range_": range_,
             "delta_sigma_abs": delta_sigma_abs,
             "obs_beta_att_lambda_on": obs_beta_att_lambda_on,
             "obs_beta_att_lambda_off": obs_beta_att_lambda_off}

delta_sigma_abs = acs.

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




