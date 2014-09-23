""" Python client for the SpaceGDN API.

`pySpaceGDN` is a Python client for the SpaceGDN game discovery network
developed for SpaceCP. The client revolves around the SpaceGDN class, which
provides the entry point to the API.

All the modules in this package contains only one class each, and these classes
have been imported into pyspacegdn/__init__.py, so they may be imported
directly from the package, like this:

>>> from pyspacegdn import SpaceGDN

Packages:
    :mod:`.requests`
        Contains the request classes

Classes:
    :class:`.SpaceGDN`
        The entry point for the client
    :class:`.Response`
        A response object for the client

Constants:
    :const:`.DEFAULT_ENDPOINT`
        The default endpoint. Set to `gdn.jamy.be` by default.
    :const:`.ELEMENT_DELIMITER`
        The delimiter to separate different elements in a filter. Set to `.`
        by default.
    :const:`.FILTER_DELIMITER`
        The delimiter to separate different filters. Set to `|` by default.

Data variables:
    :data:`.__title__`
        The title/name of this framework
    :data:`.__version__`
        The version of the framework
    :data:`.__author__`
        The author of the framework
    :data:`.__copyright__`
        The copyright string for the framework

"""

__title__ = 'pySpaceGDN'
__version__ = '2.0.1'
__author__ = 'Tobias Laundal'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 Tobias Laundal'

DEFAULT_ENDPOINT = 'gdn.jamy.be'

ELEMENT_DELIMITER = '.'
FILTER_DELIMITER = '|'

from pyspacegdn.response import Response
from pyspacegdn.spacegdn import SpaceGDN
