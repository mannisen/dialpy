#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3 functions for calculating CO2 concentration from DIAL measurements.

Created 2020-04-02, last edited 2020-04-02
Antti J Manninen
Finnish Meteorological Institute
"""

import numpy as np

# Known constants
_DELTA_RANGE = 100
_POWER_OUT_LAMBDA_ON = 1e5
_POWER_OUT_LAMBDA_OFF = 1e5


def xco2_power(range_, delta_sigma_abs, P_on, P_off, P_bkg):

    n_c = np.empty([len(range_), 1])
    n_c[:] = 0

    for i in range(len(range_)):
        n_c[i] = 1 / (2 * delta_sigma_abs * _DELTA_RANGE) * \
              np.log((P_off[i+1] - P_bkg[i+1]) / (P_on[i+1] - P_bkg[i+1]) *
                     (P_on[i] - P_bkg[i]) / (P_off[i] - P_bkg[i]))

    return n_c


def xco2_beta(delta_sigma_abs, beta_att_lambda_on, beta_att_lambda_off, P_bkg):
    """

    Args:
        delta_sigma_abs:
        beta_att_lambda_on:
        beta_att_lambda_off:
        P_bkg:

    Returns:

    """

    n_c = np.empty([len(beta_att_lambda_on), ])
    n_c[:] = 0

    # Calculate power from power of outgoing laser pulse, attenuated beta, power of background signal, range resolution
    P_on = _POWER_OUT_LAMBDA_ON * _DELTA_RANGE * beta_att_lambda_on  # + P_bkg
    P_off = _POWER_OUT_LAMBDA_OFF * _DELTA_RANGE * beta_att_lambda_off  # + P_bkg
    P_on_above = P_on[1:]
    P_off_above = P_off[1:]
    P_bkg_above = P_bkg[1:]
    P_on_below = P_on[0:-1]
    P_off_below = P_off[0:-1]
    P_bkg_below = P_bkg[0:-1]
    delta_sigma_abs = delta_sigma_abs[0:-1]

    # n_c = np.multiply(1 / (2 * delta_sigma_abs * _DELTA_RANGE),
    #                   np.log(np.multiply(np.divide((P_off_above - P_bkg_above), (P_on_above - P_bkg_above)),
    #                                      np.divide((P_on_below - P_bkg_below), (P_off_below - P_bkg_below)))))
    n_c = np.multiply(1 / (2 * delta_sigma_abs * _DELTA_RANGE),
                      np.log(np.multiply(np.divide((P_off_above), (P_on_above)),
                                         np.divide((P_on_below), (P_off_below)))))

    return n_c

