""" Usage request for `pySpaceGDN`. """

import requests
from pyspacegdn import Response


class UsageRequest(object):

    """ An `usage` request to SpaceGDN.

    This class represents and builds an `usage` request for SpaceGDN. It should
    be used to both create the request, and execute it.

    Methods:
        fetch           -- Send the request to SpaceGDN and fetch the results

    """

    def __init__(self, spacegdn):
        """ Instantiate a new `UsageRequest`.

        This method should not be called by anything outside `pySpaceGDN`.

        """
        self.spacegdn = spacegdn

    def fetch(self):
        """ Run the request and fetch the results.

        This method will compile the request, send it to the SpaceGDN endpoint
        defined with the `SpaceGDN` object and wrap the results in a `Response`
        object.

        Returns a `Response` object.

        """
        url = '/'.join(['http:/', self.spacegdn.endpoint, 'usage'])

        headers = dict()
        headers['Accept'] = 'application/json'
        headers['User-Agent'] = self.spacegdn.user_agent

        resp = requests.get(url, headers=headers)
        results = None
        if resp.ok:
            results = resp.json()

        return Response(results, resp.status_code, resp.reason)
