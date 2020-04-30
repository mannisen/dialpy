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
        delta_sigma_abs (numpy array): very crudely estimated delta absorption coefficient,

    """

    return np.repeat(8e-27 - 2.5e-28, len(range_))


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

    c_on = np.empty(400, )
    c_off = np.empty(400, )

    for i in range(len_):
        # role dice to add or subtract noise
        dice = np.random.rand()
        if dice > .5:
            c_on[i] = b_n[i] + np.random.uniform(.1, .2)
            c_off[i] = b_n[i] + np.random.uniform(.1, .2)
        else:
            c_on[i] = b_n[i] - np.random.uniform(.1, .2)
            c_off[i] = b_n[i] - np.random.uniform(.1, .2)

    # generate off channel, normalize between reasonable values beta_att (Mm-1 sr-1)
    obs_beta_off = gu.renormalize(c_off, [c_off.min(), c_off.max()], [195, 205])
    obs_beta_on = gu.renormalize(c_on, [c_on.min(), c_on.max()], [195, 205])

    # Add absorption step
    aaa = np.array([0, .005, .05, 0.1, .5, .9, .95, .995, 1])

    # generate on channel
    obs_beta_on = np.hstack((obs_beta_on[:80], obs_beta_on[80:89]-aaa*50, obs_beta_on[89:]-50))

    return obs_beta_off/1e6, obs_beta_on/1e6
