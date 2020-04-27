#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3 functions for calculating CO2 concentration from DIAL measurements.

Created 2020-04-02, last edited 2020-04-02
Antti J Manninen
Finnish Meteorological Institute
"""

import numpy as np
import matplotlib.pyplot as plt

# Known constants
_DELTA_RANGE = 25
_POWER_OUT_LAMBDA_ON = 1e42
_POWER_OUT_LAMBDA_OFF = 1e42


def xco2_power(range_, delta_sigma_abs, P_on, P_off, P_bkg):

    n_c = np.empty([len(range_), 1])
    n_c[:] = 0

    for i in range(len(range_)):
        n_c[i] = 1 / (2 * delta_sigma_abs * _DELTA_RANGE) * \
              np.log((P_off[i+1] - P_bkg[i+1]) / (P_on[i+1] - P_bkg[i+1]) *
                     (P_on[i] - P_bkg[i]) / (P_off[i] - P_bkg[i]))

    return n_c


def xco2_beta(delta_sigma_abs, beta_on=None, beta_off=None):
    """
    # last input should be P_bkg if included ..

    Args:
        delta_sigma_abs:
        beta_att_on:
        beta_att_off:
        P_bkg:

    Returns:

    """

    beta_att_on = beta_on
    beta_att_off = beta_off

    #print(type(beta_on), type(beta_off))

    #n_c = np.empty([len(beta_att_on), ])
    #n_c[:] = 0
    #n_c

    # Calculate power from power of outgoing laser pulse, attenuated beta, power of background signal, range resolution
    P_on = _POWER_OUT_LAMBDA_ON * _DELTA_RANGE * beta_att_on  # + P_bkg
    P_off = _POWER_OUT_LAMBDA_OFF * _DELTA_RANGE * beta_att_off  # + P_bkg
    #print('beta_att_on: mean {}, min {}, max {}'. format(np.mean(beta_att_on), beta_att_on.min(), beta_att_on.max()))
    #print('beta_att_off: mean {}, min {}, max {}'. format(np.mean(beta_att_off), beta_att_off.min(), beta_att_off.max()))
    #print('P_on: mean {}, min {}, max {}'. format(np.mean(P_on), P_on.min(), P_on.max()))
    #print('P_off: mean {}, min {}, max {}'. format(np.mean(P_off), P_off.min(), P_off.max()))

    P_on_above = P_on[1:]
    P_off_above = P_off[1:]
    # P_bkg_above = P_bkg[1:]
    P_on_below = P_on[:-1]
    P_off_below = P_off[:-1]
    # P_bkg_below = P_bkg[0:-1]
    delta_sigma_abs = delta_sigma_abs[:-1]
    #print('dsabs: mean {}, min {}, max {}'. format(np.mean(delta_sigma_abs), delta_sigma_abs.min(), delta_sigma_abs.max()))

    # n_c = np.multiply(1 / (2 * delta_sigma_abs * _DELTA_RANGE),
    #                   np.log(np.multiply(np.divide((P_off_above - P_bkg_above), (P_on_above - P_bkg_above)),
    #                                      np.divide((P_on_below - P_bkg_below), (P_off_below - P_bkg_below)))))

    n_c = np.multiply((1 / (2 * _DELTA_RANGE * delta_sigma_abs)),
                      np.log(np.divide(np.multiply(P_on_below, P_off_above),
                                       np.multiply(P_on_above, P_off_below))))

    return n_c

