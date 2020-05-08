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


def xco2_power(P_on, P_off, delta_sigma_abs, P_bkg=None):
    """

    Args:
        P_on:
        P_off:
        delta_sigma_abs:
        P_bkg:

    Returns:
        N_d (numpy array): Number density
        log_ratio_of_powers (numpy array): natural logarithm of ratio of powers (unitless)
    """

    # Initialize
    n_c = np.empty([len(P_on), ])
    n_c[:] = 0

    # Exclude the last for calculation
    delta_sigma_abs = delta_sigma_abs[:-1]

    # If P_bkg given, use it, otherwise assume constant value
    if P_bkg is None:
        P_bkg = np.zeros((len(P_on),))

    # Calculation the log ratio of powers
    log_ratio_of_powers = np.log(np.divide(np.multiply(P_on[:-1] - P_bkg[0:-1], P_off[1:] - P_bkg[1:]),
                                           np.multiply(P_on[1:] - P_bkg[1:], P_off[:-1] - P_bkg[0:-1])))

    # calculate concentration
    N_d = np.multiply((1 / (2 * constants.DELTA_RANGE * delta_sigma_abs)), log_ratio_of_powers)

    return N_d, log_ratio_of_powers


def xco2_beta(delta_sigma_abs, beta_att_on, beta_att_off, P_out_on=None, P_out_off=None, P_bkg=None):
    """

    Args:
        delta_sigma_abs:
        beta_att_on:
        beta_att_off:
        P_out_on:
        P_out_off:
        P_bkg:

    Returns:
        N_d (numpy array): number density
        log_ratio_of_powers (numpy array): natural logarithm of ratio of powers (unitless)

    """

    # Initialize
    n_c = np.empty([len(beta_att_on), ])
    n_c[:] = 0

    # Exclude the last for calculation
    delta_sigma_abs = delta_sigma_abs[:-1]

    # If P_out given, use it, otherwise assume constant value
    if P_out_on is None:
        P_out_on = constants.POWER_OUT_LAMBDA_ON
    if P_out_off is None:
        P_out_off = constants.POWER_OUT_LAMBDA_OFF
    if P_bkg is None:
        P_bkg = np.zeros((len(beta_att_on), ))

    # Estimate received power from Power of laser pulse, attenuated beta, power of bkg signal, delta range
    # NOTE: transmission taken into account in telescope focus correction, thus omitted here, is it OK!?
    P_on = P_out_on * constants.DELTA_RANGE * beta_att_on + P_bkg
    P_off = P_out_off * constants.DELTA_RANGE * beta_att_off + P_bkg

    # Calculation the log ratio of powers
    log_ratio_of_powers = np.log(np.divide(np.multiply(P_on[:-1] - P_bkg[0:-1], P_off[1:] - P_bkg[1:]),
                                           np.multiply(P_on[1:] - P_bkg[1:], P_off[:-1] - P_bkg[0:-1])))

    # calculate number density
    N_d = (1 / (2 * constants.DELTA_RANGE * delta_sigma_abs)) * log_ratio_of_powers

    return N_d, log_ratio_of_powers


def C_co2_ppm(N_d, T_, P_):
    """See Eq. (7) in http://dx.doi.org/10.1364/AO.52.002994

    Args:
        N_d: (float) number density (# m-3)
        T_: (float) temperature (K)
        P_: (float) pressure (atm)

    Returns:
        CO2_ppm: (float) carbon dioxide concentration (ppm)

    """

    N_L = constants.LOCHSMIDTS_NUMBER_AIR

    return (N_d / N_L) * (T_ / 273.15) * (1 / P_) * 1e6

