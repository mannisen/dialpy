#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

# Paths
PATH_TO_HITRAN = 'HITRAN_CO2_transition_data.par'
PATH_TO_TOTAL_INTERNAL_SUM = 'total_internal_partition_sum.csv'

POWER_OUT_LAMBDA_ON = 1e3  # Wrong value & probably not constant!
POWER_OUT_LAMBDA_OFF = 1e3  # Wrong value & probably not constant!

# Range resolution
DELTA_RANGE = 100  # (m)

# DIAL wavelengths
LAMBDA_ON = 1571.41 / 1e9  # (m)
LAMBDA_OFF = 1571.25 / 1e9  # (m)

# P_0
STANDARD_PRESSURE = 101325  # (Pa)
# T_0
REFERENCE_ABS_TEMPERATURE = 296.15  # (K)
# S_0
LINE_INTENSITY_AT_T_0 = 2.179e-23  # (cm mol-1)
# m'
MOLECULAR_MASS_CO2 = 43.989830  # (g)
# W_CO2
MOLAR_MASS_CO2 = 44.01  # (g mol-1)
# k
BOLTZMANNS_CONSTANT_erg = 1.3806488e-16  # (erg K-1)
BOLTZMANNS_CONSTANT = 1.3806503e-23  # (m2 kg s−2 K−1)
# h
PLANCKS_CONSTANT = 6.62606957e-27  # erg s
# c
SPEED_OF_LIGHT = 2.99792458e8  # (m s-1)
# n_0 Lochsmidt's number
LOCHSMIDTS_NUMBER_AT_1ATM_296K = 2.47937196e19  # (cm-3)
LOCHSMIDTS_NUMBER_AIR = 2.6867811e25  # (m-3)
# Q_296K for CO2
TOTAL_INTERNAL_PARTITION_SUM_296K_CO2 = 286.09
# N_A
AVOGADRO_NUMBER = 6.02214086e23  # (mol-1)
#c_2
SECOND_BLACK_BODY_RADIATION_CONSTANT = 1.43880285  # (cm K)
