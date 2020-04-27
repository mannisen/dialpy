#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt
from dialpy.pyOptimalEstimation import pyOptimalEstimation as pyOE
from dialpy.equations.differential_co2_concentration import xco2_beta
# Define the forward operator, accepts state vector X [N0,lam] as input, and
# returns measurement vector Y [Ze]
resultsOE = {}
failed = {}

def forward(X):
    # D = np.logspace(-4, -2, 50)
    #if len(X) == 2:
    #    N0log, lam = X
    #    mu = 1
    #else:
    #    N0log, lam, mu = X

    n_c, coeffs = X  # X is pd.Series type
    Ratio_P = n_c * coeffs

    #N0 = 10**N0log
    #dD = np.gradient(D)
    #N = N0 * np.exp(-lam * D**mu)
    #Z = 1e18 * np.sum(N*D**6*dD)
    return Ratio_P  # [10*np.log10(Z)]


# define names for X and Y
x_vars = ["n_c", "coeffs"]
y_vars = ["Ratio_P"]

# prior knowledge. Note that the provided numbers do not have any scientific
# meaning.

# first guess for X
coeff = 2*100*0.5  # 2 * DeltaR * delta_sigma_Abs
print('coeff {}'.format(coeff))
x_ap = [400, coeff]
# covariance matrix for X
x_cov = np.array([[.0001, 0], [0, 2]])
# covariance matrix for Y
y_cov = np.array([[.001]])

# measured observation of Y
y_obs = np.array(xco2_beta(np.array([.5, .46]), np.array([1e-4, 1e-5]), np.array([1e-4, 1e-4])))
print('y_obs {}'.format(y_obs))
#y_obs = np.array([20])

# additional data to forward function
#forwardKwArgs = {"D": np.logspace(-4, -2, 50)}

# create optimal estimation object
oe = pyOE.optimalEstimation(
    x_vars, x_ap, x_cov, y_vars, y_obs, y_cov, forward)#,
#forwardKwArgs=forwardKwArgs
#)

# run the retrieval
converged = oe.doRetrieval(maxIter=100, maxTime=10000000.0)

if converged:
    # Test whethe rthe retrieval is moderately lienar around x_truth
    #print(oe.linearityTest())

    # Show hdegrees of freedom per variable
   # print(oe.dgf_x)

    # Apply chi2 tests for retrieval quality
  #  print(oe.chiSquareTest())
    # Show RMS normalized with prior
 #   print('RMS',
 #         np.sqrt(np.mean(((oe.x_truth - oe.x_op) / oe.x_a) ** 2)))
#    print('truth', oe.x_truth)


    # Store results in xarray DataArray
    summary = oe.summarize(returnXarray=True)

#print(summary)
print(summary.x_op)
print(summary.y_op)
# plot the result
#oe.plotIterations()
#oe.summarize()
#plt.savefig("oe_result.png")


# import numpy as np
# from dialpy.pyOptimalEstimation import pyOptimalEstimation as pyOE
# from dialpy.equations.differential_co2_concentration import xco2_beta
# from dialpy.equations import absroption_corss_section as acs
# from dialpy.utilities import general_utils as gu
# from scipy.optimize import curve_fit
# import pandas as pd
# import matplotlib.pyplot as plt
#
# # Name of data fields
# x_vars = ["delta_sigma_abs", "beta_att_lambda_on", "beta_att_lambda_off"]
# y_vars = ["co2_ppm"]
#
# # variables
# # range
# range_ = np.array(np.linspace(0, 10000, num=400))
#
# # model temperature
# T_ = -range_ * 5 + 5 + 273.15  # (K)
# # model pressure
# P_ = (-range_ * .08 + 1) * 101325  # Pa
#
# # generate simulated att beta profiles
# b = np.linspace(1, 1, num=len(range_))  # -range_**2 + -range_ + 0
# b_n = b  # gu.renormalize(b, [b.min(), b.max()], [0, 1])
# c = np.empty(400, )
# for i in range(len(range_)):
#     dice = np.random.rand()
#     if dice > .5:
#         c[i] = b_n[i] + np.random.uniform(.1, .2)
#     else:
#         c[i] = b_n[i] - np.random.uniform(.1, .2)
# obs_beta_off = gu.renormalize(c, [c.min(), c.max()], [195, 205])
# aaa = np.array([0, .075, .5, .925, 1])
# obs_beta_on = np.hstack((obs_beta_off[:80], obs_beta_off[80:85]-aaa*50, obs_beta_off[85:]-50))
#
# # estimate delta_sigma
# beta_off = np.linspace(200, 200, num=len(range_))  # gu.renormalize(b_n, [b_n.min(), b_n.max()], [0, .7])
# beta_on = np.hstack((beta_off[:80], beta_off[80:85]-aaa*50, beta_off[85:]-50))
#
# beta_on[beta_on < 0] = 1
# beta_off[beta_off < 0] = 1
# power_bkg = np.repeat(1, np.shape(beta_on))
# delta_sigma_abs = np.empty((np.shape(obs_beta_off)))
#
# # for i in range(len(range_)):
# #     delta_sigma_abs[i] = acs.differential_absorption_cross_section(T_[i], P_[i])
# delta_sigma_abs[:] = .005
#
# beta_on[np.isnan(beta_on)] = 1
# beta_off[np.isnan(beta_off)] = 1
#
# priori_names = ['co2_ppm']
# co2_ppm = [np.mean(xco2_beta(delta_sigma_abs, beta_on/1e6, beta_off/1e6))]
# co2_ppm = [.5]
# #print(np.shape(tmp1))
# #print(tmp1.squeeze(),priori_names)
# #co2_ppm = pd.Series([tmp1.squeeze()], index=priori_names)
#
#
# co2_ppm_sigma = np.empty((1, 1))
# co2_ppm_sigma[:] = .01
#
# # Covariance matrix of observations
# y_vars = ["delta_sigma_abs", "beta_on", "beta_off"]
# y_obs = pd.Series([np.array(delta_sigma_abs[0])])
# print(y_obs)
# y_noise = np.array([.001, 1/1e6, 1/1e6])
# S_y = pd.DataFrame(
#     np.diag(y_noise**2),
#     index=y_vars,
#     columns=y_vars)
# #print(priori_names,co2_ppm, co2_ppm_sigma,obs_names,obs, S_y)
# #print(np.array(co2_ppm))
# # Create optimal estimation object
# #print(obs.shape)
#
# forwardKwArgs = {'beta_on': np.array(beta_on[:1]),
#                  'beta_off': np.array(beta_off[:1])}
#
# oe = pyOE.optimalEstimation(
#     priori_names,  # state variable names
#     co2_ppm,  # a priori
#     co2_ppm_sigma,  # a priori uncertainty
#     y_vars,  # measurement variable names
#     y_obs,  # observations
#     S_y,  # observation uncertainty
#     xco2_beta,  # forward Operator
#     forwardKwArgs=forwardKwArgs)  # additional function arguments
#
# #print(oe)
#
# # Do retrieval
# converged = oe.doRetrieval(maxIter=1000)
#
#
# oe.summarize()


