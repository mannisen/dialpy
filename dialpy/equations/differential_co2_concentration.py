#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3 functions for calculating CO2 concentration from DIAL measurements.

Created 2020-04-02, last edited 2020-04-02
Antti J Manninen
Finnish Meteorological Institute
"""

import numpy as np
from dialpy.equations import constants


def xco2_power(range_, delta_sigma_abs, P_on, P_off, P_bkg):

    n_c = np.empty([len(range_), 1])
    n_c[:] = 0

    for i in range(len(range_)):
        n_c[i] = 1 / (2 * delta_sigma_abs * constants.DELTA_RANGE) * \
              np.log((P_off[i+1] - P_bkg[i+1]) / (P_on[i+1] - P_bkg[i+1]) *
                     (P_on[i] - P_bkg[i]) / (P_off[i] - P_bkg[i]))

    return n_c


def xco2_beta(delta_sigma_abs, beta_att_on, beta_att_off):
    """
    # last input should be P_bkg if included ..

    Args:
        delta_sigma_abs:
        beta_att_on:
        beta_att_off:
        P_bkg:

    Returns:

    """

    #n_c = np.empty([len(beta_att_on), ])
    #n_c[:] = 0

    # Power of outgoing laser pulse, attenuated beta, power of background signal, range resolution
    # Transmission taken into account in telescope focus correction, thus omitted here
    P_on = constants.POWER_OUT_LAMBDA_ON * constants.DELTA_RANGE * beta_att_on  # + P_bkg
    P_off = constants.POWER_OUT_LAMBDA_OFF * constants.DELTA_RANGE * beta_att_off  # + P_bkg

    # Extract values for x(R) and x(R+deltaR)
    P_on_above = P_on[1:]
    P_off_above = P_off[1:]
    # P_bkg_above = P_bkg[1:]
    P_on_below = P_on[:-1]
    P_off_below = P_off[:-1]
    # P_bkg_below = P_bkg[0:-1]
    delta_sigma_abs = delta_sigma_abs[:-1]

    # When the background noise is known, add in the P_bkg
    # n_c = np.multiply(1 / (2 * delta_sigma_abs * _DELTA_RANGE),
    #                   np.log(np.multiply(np.divide((P_off_above - P_bkg_above), (P_on_above - P_bkg_above)),
    #                                      np.divide((P_on_below - P_bkg_below), (P_off_below - P_bkg_below)))))

    n_c = np.multiply((1 / (2 * constants.DELTA_RANGE * delta_sigma_abs)),
                      np.log(np.divide(np.multiply(P_on_below, P_off_above),
                                       np.multiply(P_on_above, P_off_below))))

    return n_c

