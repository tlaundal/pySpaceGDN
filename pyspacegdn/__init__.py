""" Python client for the SpaceGDN API.

`pySpaceGDN` is a Python client for the SpaceGDN game discovery network
developed for SpaceCP. The client revolves around the SpaceGDN class, which
provides the entry point to the API.

All the modules in this package contains only one class each, and these classes
have been imported into pyspacegdn/__init__.py, so they may be imported
directly from the package, like this:

>>> from pyspacegdn import SpaceGDN

Packages:
    `requests`
        Contains the request classes

Classes:
    `SpaceGDN`
        The entry point for the client
    `Response`
        A response object for the client

Constants:
    `DEFAULT_ENDPOINT`
        The default endpoint. Set to `gdn.jamy.be` by default.
    `ELEMENT_DELIMITER`
        The delimiter to separate different elements in a filter. Set to `.`
        by default.
    `FILTER_DELIMITER`
        The delimiter to separate different filters. Set to `|` by default.

"""

__title__ = 'pySpaceGDN'
__version__ = '2.0.0-dev'
__author__ = 'Tobias Laundal'
__copyright__ = 'Copyright 2014 Tobias Laundal'

DEFAULT_ENDPOINT = 'gdn.jamy.be'

ELEMENT_DELIMITER = '.'
FILTER_DELIMITER = '|'

from pyspacegdn.response import Response
from pyspacegdn.spacegdn import SpaceGDN
