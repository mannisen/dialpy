#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3 functions for calculating CO2 concentration from DIAL measurements.

Created 2020-05-06
Antti J Manninen
Finnish Meteorological Institute
"""

import numpy as np
import pandas as pd
from dialpy.utilities import general_utils as gu
from dialpy.equations import constants


def read_hitran_data(nu_):
    """Reads parameters from the file provided by the HITRAN data (in csv format)

    Args:
        nu_:

    Returns:
        nu_0:
        S_0:
        gamma_0:
        E_:
        a_:

    """

    data = pd.read_csv(constants.PATH_TO_HITRAN, delimiter='\t', header=None)

    # Columns:  Isotopologue nu S A gamma_air gamma_self E" n_air delta_air J' J"
    idx, _ = gu.find_nearest(np.array(data.values[:, 1]), nu_)
    nu_0 = data.values[idx, 1]
    S_0 = data.values[idx, 2]
    gamma_0 = data.values[idx, 5] / 1e2  # (m / 1 atm)
    E_ = data.values[idx, 6] / 1e2
    a_ = data.values[idx, 7]

    return nu_0, S_0, gamma_0, E_, a_


def shifted_spectral_line(nu_ij, delta_air, P_total):
    """Calculates the shifted spectral line center nu*_ij due to pressure compared to the unperturbed value specified
    in the HITRAN database.

    Args:
        nu_ij (float): vacuum wavenumber (cm-1)
        delta_air (float): air-broadened half width at half maximum (HWHM), (cm-1 atm-1)
        P_total (float): total atmospheric pressure (1 atm)

    Returns:
        nu*_ij (float): pressure shifted spectral line (cm-1)

    """

    return nu_ij + delta_air + P_total


def total_internal_partition_sum(T_):
    """

    Args:
        T_:

    Returns:

    """

    data = pd.read_csv(constants.PATH_TO_TOTAL_INTERNAL_SUM, delimiter=',', header=None)
    idx, _ = gu.find_nearest(np.array(data.values[:, 0]), T_)

    return float(data.values[idx, 1])


def spectral_line_intensity(range_, S_0_ij, Q_T, E_, T_, nu_ij, co2_ppm):
    """

    Args:
        range_ (float): range from instrument (m)
        S_ij: (float):
        Q_296K: (float): total internal partition sum for the temperature of 296 K
        Q_T: (float): total internal partition sum value for the calculation temperature
        c_2: (float): c2=c⋅h/k  = 1.43880285 (cm · K) econd black body radiation constant
        E_: (float):
        T_: (float): temperature (K)
        nu_ij: (float):
        co2_ppm (float):

    Returns:
        S_L (float):

    """
    Q_296K = constants.TOTAL_INTERNAL_PARTITION_SUM_296K_CO2
    B = 0.984204  # isotope abundance of 12C16O2, the most abundant
    B_T = B  # in terrestrial atmosphere
    N_L = constants.LOCHSMIDTS_NUMBER_AT_1ATM_296K
    L_ = range_ * 1e2 * 2  # 1e2 for m --> cm, 2 for round trip
    P_mol = 1 * co2_ppm/1e4  # (atm), ppm --> % and multiplied with 1 atm
    k_ = constants.BOLTZMANNS_CONSTANT
    h_ = constants.PLANCKS_CONSTANT
    c_2 = constants.SPEED_OF_LIGHT * 1e2 * h_ / k_  # c_2 second black body radiation constant (cm K)

    # S*_ij
    Ss_ij = S_0_ij * (Q_296K / Q_T) * (np.exp(-c_2 * E_ / T_) / np.exp(-c_2 * E_ / 296)) * \
           ((1 - np.exp(-c_2 * nu_ij / T_)) / (1 - np.exp(-c_2 * nu_ij / 296)))

    # S_L
    return Ss_ij * (B / B_T) * (296 / T_) * N_L * P_mol * L_


def doppler_HWHM(nu_ij, T_):
    """

    Args:
        nu_ij (float):
        T_ (float): temperature (K)

    Returns:
        alpha_Doppler (float):

    """

    c_ = constants.SPEED_OF_LIGHT
    N_A = constants.AVOGADRO_NUMBER
    k_ = constants.BOLTZMANNS_CONSTANT
    W_g = constants.MOLAR_MASS_CO2

    return nu_ij / c_ * np.sqrt((2 * N_A * k_ * T_ * np.log(2)) / (1e-3 * W_g))


