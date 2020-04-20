#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3 functions for calculating CO2 concentration from DIAL measurements.

Created 2020-04-20
Antti J Manninen
Finnish Meteorological Institute
"""

import numpy as np
from scipy.integrate import quad

temperature = 293  # (K) = 20 celsius


def line_intensity(S_0, T_0, T_, h_, c_, nu_0, k_, E_):
    """See Johnson et al. (2013) Eq. (4) http://dx.doi.org/10.1364/AO.52.002994,
    and Browell et al. (1991) Eq. (1) https://doi.org/10.1364/AO.30.001517

    Args:
        S_0: line strength (intensity) at temperature T_0 = 296,15 (K)
        T_0: 296,15 (K)
        T_: temperature (K)
        h_: Planck's constant
        c_: speed of light
        nu_0: wavenumber (central) at T_0 = 296,15 (K) and P_0 = 101325 (Pa)
        k_: Boltzmann's constant
        E_: lower energy state of the transition

    Returns:
        S_: line intensity

    """

    S_ = S_0 * (T_0/T_)**(3/2) * \
         ((1 - np.exp(-h_ * c_ * nu_0 / (k_ * T_))) / (1 - np.exp(-h_ * c_ * nu_0 / (k_ * T_0)))) * \
         np.exp((h_ * c_) / k_ * (1 / T_0 - 1 / T_) * E_)

    return S_


def pressure_broadened_linewidth(gamma_0, P_, P_0, T_0, T_, a_):
    """See Browell et al. (1991) Eq. (2) https://doi.org/10.1364/AO.30.001517

    Args:
        gamma_0: Lorentz linewidth at temperature T_0 = 296,15 (K) and pressure P_0 = 101325 (Pa)
        P_: pressure (Pa)
        P_0: 101325 (Pa)
        T_0: 296,15 (K)
        T_: temperature (K)
        a_: linewidth temperature-dependence parameter

    Returns:
        gamma_L: pressure broadened linewidth at temperature T_ and pressure P_

    """

    gamma_L = gamma_0 * (P_ / P_0) * (T_0 / T_)**a_

    return gamma_L


def doppler_broadened_linewidth(nu_0, c_, k_, T_, m_):
    """Half-width at half maximum (HWHM), see See Johnson et al. (2013) p. 2996 http://dx.doi.org/10.1364/AO.52.002994,
    and Browell et al. (1991) p. 1518 https://doi.org/10.1364/AO.30.001517

    Args:
        nu_0: wavenumber (central) at T_0 = 296,15 (K) and P_0 = 101325 (Pa)
        c_: speed of light
        k_: Boltzmann's constant
        T_: temperature (K)
        m_: mass of molecule (carbon dioxide in the case of CO2-DIAL)

    Returns:
        gamma_D: Doppler broadened linewidth (HWHM)

    """

    gamma_D = (nu_0 / c_) * (2 * k_ * T_ * np.log(2) / m_)**(1/2)

    return gamma_D


def integrand(t, x, y):
    """Integrand function for integral calculated in the absorption cross section function

    Args:
        t: variable of integration
        x: (gamma_L / gamma_D)**2 * np.log(2)
        y: ((nu-nu_0)/gamma_D) * np.log(2)**(1/2)

    Returns:

    """

    return np.exp(-t**2) / (x+(y-t)**2)


def abs_cross_section(S_, gamma_L, gamma_D, nu, nu_0):
    """

    Args:
        S_: line intensity
        gamma_L: pressure broadened linewidth at temperature T_ and pressure P_
        gamma_D: Doppler broadened linewidth (HWHM)
        nu: wavenumber at which the cross section is being calculated
        nu_0: wavenumber (central) at T_0 = 296,15 (K) and P_0 = 101325 (Pa)

    Returns:
        sigma_abs: absorption cross section

    """

    x = (gamma_L / gamma_D)**2 * np.log(2)
    y = ((nu-nu_0) / gamma_D) * np.log(2)**(1/2)
    sigma_abs = S_ * (np.log(2) / np.pi**(3/2)) * (gamma_L / gamma_D**2) * quad(integrand, -np.inf, np.inf,
                                                                                args=(x, y))[0]

    return sigma_abs
