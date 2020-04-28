#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from dialpy.utilities import general_utils as gu


def sim_range(min_=0, max_=10, len_=400):
    """

    Args:
        min_ (float): min range in mk
        max_ (float): max range in mk
        len_ (int): len of range

    Returns:
        range_ (numpy array): range from instrument

    """

    return np.linspace(0, 10, len_)


def sim_delta_sigma_abs(range_):
    """

    Args:
        range_ (numpy array): range from instrument

    Returns:
        delta_sigma_abs (numpy array): very crudely estimated differential absorption coefficient,
        see Han et al. (2017), Fig. 1, https://www.doi.org/10.1109/TGRS.2017.2720618

    """

    return .6/10*range_  # very close to the ground


def sim_noisy_beta_att(len_=400, type_='poly1'):
    """

    Args:
        len_ (int): len of arrays
        type_ (str): Optional. 'poly1' or 'poly2'

    Returns:
        beta_att_off (numpy array): estimated attenuated backscatter coefficient, off channel
        beta_att_on (numpy array): estimated attenuated backscatter coefficient, on channel

    """

    # generate simulated att beta profiles
    if type_ is 'poly1':
        b = np.linspace(1, 1, num=len_)
        b_n = b
    elif type_ is 'poly2':
        b = -np.linspace(0, 1, len_) ** 2 + -np.linspace(0, 1, len_) + 0
        b_n = gu.renormalize(b, [b.min(), b.max()], [0, 1])
    else:
        raise ValueError("Optional input type_= can be 'poly1' or 'poly2' ")

    c = np.empty(400, )
    for i in range(len_):
        # role dice to add or subtract noise
        dice = np.random.rand()
        if dice > .5:
            c[i] = b_n[i] + np.random.uniform(.1, .2)
        else:
            c[i] = b_n[i] - np.random.uniform(.1, .2)

    # generate off channel, normalize between reasonable values beta_att (Mm-1 sr-1)
    obs_beta_off = gu.renormalize(c, [c.min(), c.max()], [195, 205])

    # Add absorption step
    aaa = np.array([0, .075, .5, .925, 1])

    # generate on channel
    obs_beta_on = np.hstack((obs_beta_off[:80], obs_beta_off[80:85]-aaa*50, obs_beta_off[85:]-50))

    return obs_beta_off/1e6, obs_beta_on/1e6
