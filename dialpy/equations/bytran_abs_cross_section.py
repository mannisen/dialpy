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
from scipy.integrate import quad
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

    data = pd.read_csv(constants.PATH_TO_HITRAN, delimiter=',', header=None)
    idx, _ = gu.find_nearest(np.array(data.values[:, 0]), T_)

    return data.values[idx, 1]


def recalculate_spectral_line_intensity(S_ij, Q_T, E_, T_, nu_ij):
    """

    Args:
        S_ij: (float):
        Q_296K: (float): total internal partition sum for the temperature of 296 K
        Q_T: (float): total internal partition sum value for the calculation temperature
        c_2: (float): c2=c⋅h/k  = 1.43880285 (cm · K) econd black body radiation constant
        E_: (float):
        T_: (float): temperature (K)
        nu_ij: (float):

    Returns:
        S*_ij (float):

    """
    c_2 = constants.SECOND_BLACK_BODY_RADIATION_CONSTANT
    Q_296K = constants.TOTAL_INTERNAL_PARTITION_SUM_296K_CO2

    return S_ij * (Q_296K / Q_T) * (np.exp(-c_2 * E_ / T_) / np.exp(-c_2 * E_ / 296)) * \
           ((1 - np.exp(-c_2 * nu_ij / T_)) / (1 - np.exp(-c_2 * nu_ij / 296)))


def
