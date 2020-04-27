#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

PATH_TO_HITRAN = 'HITRAN_CO2_transition_data.par'

# Instrumental
DELTA_RANGE = 100  # (m)
LAMBDA_ON = 1.57141e-6  # (m)
LAMBDA_OFF = 1.57125e-6  # (m)
POWER_OUT_LAMBDA_ON = 1e42  # Wrong value & probably not constant!
POWER_OUT_LAMBDA_OFF = 1e42  # Wrong value & probably not constant!

# nu_0
CENTRAL_WAVELENGTH = 6360  # Probably wrong value

# P_0
STANDARD_PRESSURE = 101325  # (Pa)
# T_0
REFERENCE_ABS_TEMPERATURE = 296.15  # (K)
# S_0
LINE_INTENSITY_AT_T_0 = 2.179e-23  # (cm mol-1)
# m'
MOLECULAR_MASS_CO2 = 43.989830  # (g)
# k
BOLTZMANNS_CONSTANT = 1.3806488e-16  # (erg K-1)
# h
PLACKS_CONSTANT = 6.62606957e-27  # erg s
# c
SPEED_OF_LIGHT = 2.99792458e8  # (m s-1)
