""" SpaceGDN class for `pySpaceGDN`. """

from __future__ import absolute_import

from requests.utils import default_user_agent
import pyspacegdn
from pyspacegdn.requests import Request, FindRequest


class SpaceGDN(object):

    """ The main class for pySpaceGDN.

    An instance of this class is the entrypoint for pySpaceGDN. Through this
    class, most request types defined by SpaceGDN can be sent to a SpaceGDN
    host.

    Methods:
        :meth:`.find`
            Create a find request
        :meth:`.usage`
            Create an usage request

    Attributes:
        :attr:`.client_name`
            The name of the client that created this instance. If the client
            name is not set, this will be `Uknown`
        :attr:`.client_version`
            The version of the client that created this instance. If the client
            version is not set, this will be `uknown`
        :attr:`.endpoint`
            The endpoint this instance relates to.
        :attr:`.user_agent`
            The user agent string for this client.

    """

    def __init__(self, client_name='Uknown', client_version='uknown',
                 endpoint=pyspacegdn.DEFAULT_ENDPOINT):
        """ Instantiate a new SpaceGDN client.

        There are no required arguments. The client name and version arguments
        are used to set the user agents, and should be set when using
        pySpaceGDN for other things than testing.

        Optional arguments:
            `client_name` (`str`)
                The name of the client using this instance. Defaults to
                `Uknown`.
            `client_version` (`str`)
                The version of the client using this instance. Defaults to
                `uknown`.
            `endpoint` (`str`)
                The endpoint to connect to. Defaults to
                :const:`pyspacegdn.DEFAULT_ENDPOINT` in :mod:`pyspacegdn`.

        """
        self.client_name = client_name
        self.client_version = client_version
        self.endpoint = endpoint

        self.user_agent = self._create_user_agent()

    def _create_user_agent(self):
        """ Create the user agent and return it as a string. """
        user_agent = '{}/{} {}'.format(pyspacegdn.__title__,
                                       pyspacegdn.__version__,
                                       default_user_agent())
        if self.client_name:
            user_agent = '{}/{} {}'.format(self.client_name,
                                           self.client_version, user_agent)
        return user_agent

    def find(self):
        """ Create and return a new :class:`pyspacegdn.requests.FindRequest`.
        """
        return FindRequest(self)

    def usage(self):
        """ Create and return a new :class:`pyspacegdn.requests.UsageRequest`.
        """
        return Request(self).set_path('v2/usage')
