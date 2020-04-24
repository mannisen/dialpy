#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:54:08 2019

@author: manninan
"""

import numpy as np
import re
import os


def renormalize(n, range1, range2):
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]


def normalize_between(values, actual_bounds, desired_bounds):
    """

    Args:
        values:
        actual_bounds:
        desired_bounds:

    Returns:

    """
    return [desired_bounds[0] +
            (x - actual_bounds[0]) *
            (desired_bounds[1] - desired_bounds[0]) /
            (actual_bounds[1] - actual_bounds[0]) for x in values]


def find_nearest(a, a0):
    """Element in nd array `a` closest to the scalar value `a0`

    Args:
        a: look from
        a0: look for

    Returns:
        idx: index of nearest value
        val: nearest value

    """
    idx = np.abs(a - a0).argmin()
    return idx, a.flat[idx]


def look_for_from(look_for, look_from):
    """Looks for a string from list of strings.

    Args:
        look_for (str): string to look for
        look_from (list): list of strings (str) to look from

    Returns:
        indices (int/list): indices (int) where found

    """

    try:
        isinstance(look_from, list)
    except False:
        raise ValueError('First input must be a list (of strings).')
    try:
        isinstance(look_for, str)
    except False:
        raise ValueError('Second input must a string.')
        
    indices = [i for i, x in enumerate(look_from) if look_for in x]

    return indices[0] if len(indices) == 1 else indices


def camel2snake(str_in):
    """Converts str from CamelFormat to snake_format.

    Args:
        str_in: (str) String in CamelFormat

    Returns:
        str_out: (str) String in snake_format

    """

    words = str_in.splitlines()

    reg_ = r"(.+?)([A-Z])"

    def snake(match):
        return match.group(1).lower() + "_" + match.group(2).lower()

    results = [re.sub(reg_, snake, w, 0) for w in words]
    str_out = results[0]

    return str_out


def list2str(in_list):
    """Converts list of strings to string preserving quotation marks
    """
    ret_list = "'" + "', '".join(in_list) + "'"

    return ret_list


def list_files(path_, file_type, starting_pattern=None):
    """A general function for listing files in a folder.

    Args:
        path_ (str): path to folder
        file_type (str): file type. e.g. ".nc"
        starting_pattern (str): "VADprof", "if t = 20170431 --> t.strftime("%Y%m%d")"

    Returns:
        file_info (dict): dictionary listing file names, full paths and total number of files

    """

    full_paths = []
    file_names = []
    # List files and get only files for which parameters are valid
    try:
        for entry in os.scandir(path_):
            if starting_pattern is not None:
                if entry.name.endswith(file_type) and entry.name.startswith(starting_pattern):
                    full_paths.append(os.path.join(path_, entry.name))
                    file_names.append(entry.name)
            else:
                if entry.name.endswith(file_type):
                    full_paths.append(os.path.join(path_, entry.name))
                    file_names.append(entry.name)

    except FileNotFoundError as err:
        raise print("FileNotFoundError: {0}".format(err))

    return {'file_names': file_names,
            'full_paths': full_paths,
            'number_of_files': len(full_paths)}


def rreplace(s, old, new, occurrence):
    """Replaces the last occurrence of an expression in a string.
    https://stackoverflow.com/a/2556252

    Args:
        s (str):
        old (str):
        new (str):
        occurrence (int):

    Returns:
        li (str):

    """
    li = s.rsplit(old, occurrence)
    return new.join(li)


def copy_attributes(obj_from, obj_to, att_names):
    for n in att_names:
        if hasattr(obj_from, n) and getattr(obj_from, n) is not None:
            v = getattr(obj_from, n)
            setattr(obj_to, n, v)
