#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3 functions for calculating CO2 concentration from DIAL measurements.

Created 2020-05-06
Antti J Manninen
Finnish Meteorological Institute

DOCUMENTATION: http://www.bytran.org/howtolbl.htm

"""

import numpy as np
import pandas as pd
from dialpy.utilities import general_utils as gu
from dialpy.equations import constants
from scipy.integrate import quad


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
    gamma_air = data.values[idx, 4]  # (cm atm-1)
    gamma_self = data.values[idx, 5]  # (cm atm-1)
    E_ = data.values[idx, 6]  # (cm-1)
    n_air = data.values[idx, 7]  # (cm-1)
    delta_air = data.values[idx, 8]  # (cm-1)

    return nu_0, S_0, gamma_air, gamma_self, E_, n_air, delta_air


def shifted_spectral_line(nu_ij, delta_air, P_):
    """Calculates the shifted spectral line center nu*_ij due to pressure compared to the unperturbed value specified
    in the HITRAN database.

    Args:
        nu_ij: (float) vacuum wavenumber (cm-1)
        delta_air: (float) air-broadened half width at half maximum (HWHM), (cm-1 atm-1)
        P_: (float) total atmospheric pressure (1 atm)

    Returns:
        nu*_ij: (float) pressure shifted spectral line (cm-1)

    """

    return nu_ij + delta_air + P_


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
        range_: (float) range from instrument (m)
        S_0_ij: (float)
        Q_T: (float) total internal partition sum value for the calculation temperature
        E_: (float)
        T_: (float) temperature (K)
        nu_ij: (float)
        co2_ppm: (float)

    Returns:
        S_L: (float)

    """
    Q_296K = constants.TOTAL_INTERNAL_PARTITION_SUM_296K_CO2
    B = 0.984204  # isotope abundance of 12C16O2, the most abundant
    B_T = B  # in terrestrial atmosphere
    N_L = constants.LOCHSMIDTS_NUMBER_AT_1ATM_296K
    L_ = range_ * 1e2 * 2  # 1e2 for m --> cm, 2 for round trip
    P_mol = 1 * co2_ppm/1e4  # (atm), ppm --> % and multiplied with 1 atm
    c_2 = constants.SECOND_BLACK_BODY_RADIATION_CONSTANT  # (cm K)

    # S*_ij
    Ss_ij = S_0_ij * (Q_296K / Q_T) * (np.exp(-c_2 * E_ / T_) / np.exp(-c_2 * E_ / 296)) * \
           ((1 - np.exp(-c_2 * nu_ij / T_)) / (1 - np.exp(-c_2 * nu_ij / 296)))

    # S_L
    return Ss_ij * (B / B_T) * (296 / T_) * N_L * P_mol * L_


def doppler_HWHM(nu_ij, T_):
    """

    Args:
        nu_ij: (float)
        T_: (float) temperature (K)

    Returns:
        alpha_doppler: (float)

    """

    c_ = constants.SPEED_OF_LIGHT  # (m s-1)
    N_A = constants.AVOGADRO_NUMBER  # (mol-1)
    k_ = constants.BOLTZMANNS_CONSTANT  # (m2 kg s−2 K−1)
    W_g = constants.MOLAR_MASS_CO2  # (g mol-1)

    return nu_ij / c_ * np.sqrt((2 * N_A * k_ * T_ * np.log(2)) / (1e-3 * W_g))


def lorentzian_HWHM(T_, n_air, gamma_air, P_, P_mol, gamma_self):
    """

    Args:
        T_:
        n_air:
        gamma_air:
        P_:
        P_mol:
        gamma_self:

    Returns:
        gamma: (float)

    """

    return (296 / T_)**n_air * (gamma_air * (P_ - P_mol) + gamma_self * P_mol)


def f_doppler(alpha_doppler, nu, nu_ij_shifted):
    """In the low-pressure environment of the upper atmosphere Doppler-broadening dominates the line shape and a
    Gaussian profile can be assumed

    Args:
        alpha_Doppler: (float)
        nu: (float)
        nu_ij_shifted: (float)

    Returns:
        f_doppler: (float) Doppler lineshape profile

    """

    return np.sqrt(np.log(2) / (np.pi * alpha_doppler**2)) * \
           np.exp(-(((nu - nu_ij_shifted)**2 * np.log(2)) / (alpha_doppler**2)))


def f_lorentz(gamma, nu, nu_ij_shifted):
    """In the lower atmosphere, pressure broadening of spectral lines dominates and if a Lorentz profile can be assumed,

    Args:
        gamma: (float)
        nu: (float) wavenumber (cm-1)
        nu_ij_shifted: (float) pressure shifted wavenumber (cm-1)

    Returns:
        f_lorentz: (float)

    """

    return 1 / np.pi * (gamma / (gamma**2 + (nu - nu_ij_shifted)**2))


def integrand_K_x_y(t, x, y):
    """Integrand function for integral calculated in the absorption cross section function

    Args:
        t: (float) variable of integration
        x: (float)
        y: (float)

    Returns:

    """

    return np.exp(-t**2) / (y**2+(x-t)**2)


def integrand_L_x_y(t, x, y):
    """Integrand function for integral calculated in the absorption cross section function

    Args:
        t: (float) variable of integration
        x: (float)
        y: (float)

    Returns:

    """

    return ((x - t) * np.exp(-t**2)) / (y**2+(x-t)**2)


def voigt_abrarov_quine(x, y):
    """See Abrarov and Quine (2015), http://dx.doi.org/10.5539/jmr.v7n2p163

    Args:
        x: (float)
        y: (float)

    Returns:

    """

    coeff = np.array([2.307372754308023e-001, 4.989787261063716e-002, 1.464495070025765e+000,
                      7.760531995854886e-001, 4.490808534957343e-001, -3.230894193031240e-001,
                      4.235506885098250e-002, 1.247446815265929e+000, -5.397724160374686e-001,
                      -2.340509255269456e-001, 2.444995757921221e+000, -6.547649406082363e-002,
                      -4.557204758971222e-002, 4.041727681461610e+000, 2.411056013969393e-002,
                      5.043797125559205e-003, 6.037642585887094e+000, 4.001198804719684e-003,
                      1.180179737805654e-003, 8.432740471197681e+000, -5.387428751666454e-005,
                      1.754770213650354e-005, 1.122702133739336e+001, -2.451992671326258e-005,
                      -3.325020499631893e-006, 1.442048518447414e+001, -5.400164289522879e-007,
                      -9.375402319079375e-008, 1.801313201244001e+001, 1.771556420016014e-008,
                      8.034651067438904e-010, 2.200496182129099e+001, 4.940360170163906e-010,
                      3.355455275373310e-011, 2.639597461102705e+001, 5.674096644030151e-014])

    mMax = 12
    varsigma = 2.75  # define the shift constant
    y = np.abs(y) + varsigma / 2
    arr1 = y.ˆ2 - x.ˆ2  # define 1st repeating array
    arr2 = x.ˆ2 + y.ˆ2  # define 2nd repeating array
    arr3 = arr2.ˆ2  # define 3rd repeating array
    VF = 0  # initiate VF
    for m in range(mMax):
        VF += + (coeff[m, 0] * (coeff[m, 1] + arr1) +
                 coeff[m, 2] * y * (coeff[m, 1] + arr2)) / (coeff[m, 1]**2 +
                                                            2 * coeff[m, 1] * arr1 + arr3)

    return VF


def voigt(nu, nu_ij_shifted, alpha_doppler, gamma):

    x_ = (np.sqrt(np.log(2)) * (nu - nu_ij_shifted)) / alpha_doppler
    y_ = (np.sqrt(2) * gamma) / alpha_doppler

    return voigt_abrarov_quine(x_, y_)

def absorption_coefficient(range_, T_, co2_ppm):



    S_L = spectral_line_intensity(range_, S_0_ij, Q_T, E_, T_, nu_ij, co2_ppm):


    return S_L * f_voigt



