"""
pyart.graph.cm_colorblind
=========================
Colorblind friendly radar colormaps
.. autosummary::
    :toctree: generated/
    _generate_cmap
Available colormaps, reversed versions are also provided, these
colormaps are available within matplotlib with names pyart_COLORMAP':
    * HomeyerRainbow
"""

import matplotlib as mpl
import matplotlib.colors as colors
import numpy as np

from dialpy.utilities.cm import _reverse_cmap_spec
from dialpy.utilities._cm_colorblind import datad


def _generate_cmap(name, lutsize):
    """Generates the requested cmap from it's name *name*.  The lut size is
    *lutsize*."""

    spec = datad[name]

    # Generate the colormap object.
    if isinstance(spec, dict):
        if 'red' in spec:
            return colors.LinearSegmentedColormap(name, spec, lutsize)
        else:
            return colors.LinearSegmentedColormap.from_list(name, spec, lutsize)

    elif isinstance(spec, np.ndarray):
        return colors.LinearSegmentedColormap(name, spec, lutsize)


cmap_d = dict()

# reverse all the colormaps.
# reversed colormaps have '_r' appended to the name.

LUTSIZE = mpl.rcParams['image.lut']

# need this list because datad is changed in loop
_cmapnames = list(datad.keys())

# Generate the reversed specifications ...

for cmapname in _cmapnames:
     spec = datad[cmapname]
     spec_reversed = _reverse_cmap_spec(spec)
     datad[cmapname + '_r'] = spec_reversed

# Precache the cmaps with ``lutsize = LUTSIZE`` ...

# Use datad.keys() to also add the reversed ones added in the section above:
for cmapname in datad.keys():
    cmap_d[cmapname] = _generate_cmap(cmapname, LUTSIZE)

locals().update(cmap_d)

# register the colormaps so that can be accessed with the names pyart_XXX
for name, cmap in cmap_d.items():
    full_name = 'pyart_' + name
    mpl.cm.register_cmap(name=full_name, cmap=cmap)
