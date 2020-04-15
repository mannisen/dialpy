#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3 functions for calculating CO2 concentration from DIAL measurements.

Created 2020-04-02, last edited 2020-04-02
Antti J Manninen
Finnish Meteorological Institute
"""

import numpy as np

# Known constants
_DELTA_RANGE = 30
_POWER_OUT_LAMBDA_ON = 1
_POWER_OUT_LAMBDA_OFF = 1


def xco2(range_, delta_sigma_abs, beta_att_lambda_on, beta_att_lambda_off, power_background):

    n_c = np.empty([len(range_), 1])
    n_c[:] = 0
    power_in_lambda_on = _POWER_OUT_LAMBDA_ON * _DELTA_RANGE * beta_att_lambda_on + power_background
    power_in_lambda_off = _POWER_OUT_LAMBDA_OFF * _DELTA_RANGE * beta_att_lambda_off + power_background

    for i in range(len(range_)):

        n_c[i] = 1 / (2 * delta_sigma_abs * _DELTA_RANGE) * \
            np.log((power_in_lambda_off[i+1] - power_background) / (power_in_lambda_on[i+1] - power_background) *
                   (power_in_lambda_on[i] - power_background) / (power_in_lambda_off[i] - power_background))

    return n_c


