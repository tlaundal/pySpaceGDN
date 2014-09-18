""" Request classes for `pySpaceGDN`.

This package contains classes representing requests to the SpaceGDN API. All
the classes are placed in separate modules, but they are imported into the
package for convenience. This means that you can import the classes directly
from the package, like this:

>>> from pyspacegdn.requests import FindRequest

"""

from pyspacegdn.requests.request import Request
from pyspacegdn.requests.find_request import FindRequest
