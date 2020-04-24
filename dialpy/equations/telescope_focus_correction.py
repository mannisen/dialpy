#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3 functions for DIAL processing chain.

Created 2020-04-02, last edited 2020-04-02
Antti J Manninen
Finnish Meteorological Institute
"""

import numpy as np

_ROO_ZERO = 1
_PLANCK_CONSTANT = 1
_BOLTZMANN_CONSTANT = 1
_RECEIVER_BANDWIDTH = 1


def effective_receiver_area(range_, D_eff, f_eff, lambda_):
    """Calculate effective receiver area as a function of range based on the estimated effective laser beam diameter,
    effective focal length, and laser wavelength. For more detail see Pentikainen et al. (2020) Eq. (2),
    https://doi.org/10.5194/amt-2019-491

    Args:
        range_ (np.ndarray): Range from the instrument (m)
        D_eff (float):  Effective laser beam diameter (m) estimated by using Pentikainen et al. (2020) method
        f_eff (float): Effective focal length (m) estimated with using Pentikainen et al. (2020) method
        lambda_ (float): Wavelength of the laser (m)

    Returns:
        A_e (np.ndarray): Effective receiver area as a function of range (m)

    """

    A_e = np.divide(np.pi * D_eff**2, 4 * (1 + (np.divide(np.pi * D_eff**2, 4 * lambda_ * range_))**2) *
                    (1 - range_ / f_eff)**2 +
                    (D_eff / (2 * _ROO_ZERO))**2)

    return A_e


def focus_function(range_, A_e):
    """Calculates the telescope focus function as a function of range: T_f = A_e(r) / r^2. For more details see
    Pentikainen et al. (2020) Eq. (3), https://doi.org/10.5194/amt-2019-491

    Args:
        range_ (numpy.ndarray): Range from the instruments (m)
        A_e (np.ndarray): Effective receiver area (m)

    Returns:
        T_f (np.ndarray): Telescope focus function (unitless)

    """

    T_f = np.divide(A_e, range_**2)

    return T_f


def attenuated_backscatter_coefficient(snr_, T_f, lambda_, eta_, E_):
    """Calculates attenuated backscatter coefficients given the telescope focus function T_f. For more details see
    Pentikainen et al. (2020) Eq. (4), https://doi.org/10.5194/amt-2019-491

    Args:
        snr_ (np.ndarray): Background corrected signal-to-noise ratio (dB)
        T_f (np.ndarray): Telescope focus function (unitless)
        lambda_ (float): Wavelength of the laser (m)
        eta_ (float): Heterodyne efficiency (unitless)

    Returns:
        beta_att : np.ndarray
            Calibrated attenuated backscatter coefficients (m-1 sr-1)

    """

    h = _PLANCK_CONSTANT
    nu_ = optical_frequency(lambda_)
    B = _BOLTZMANN_CONSTANT
    c = _SPEED_OF_LIGHT

    beta_att = 2 * h * nu_ * B / (eta_ * c * E_) * np.divide(snr_, T_f)

    return beta_att
