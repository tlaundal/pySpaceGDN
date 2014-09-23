""" Generic request for `pySpaceGDN`. """

import requests
from pyspacegdn import Response


class Request(object):

    """ A generic request to SpaceGDN.

    This class provides a base to build other request classes on, it can also
    be used on its own for very simple requests.

    Request classes that build on this one should just use this class's methods
    to set the path, `GET` and/or `POST` parameters. The `fetch` method can
    then be used to fetch the results.

    Headers are handled autmatically. The request type is guessed by looking at
    the `POST` parameters. If there are no `POST` parameters, a `GET` request
    will be carried out when `fetch` is called.

    All methods will `return self`.

    Methods:
        :meth:`.set_path`
            Set the path to query
        :meth:`.add_post_param`
            Add a HTTP POST parameter
        :meth:`.add_get_param`
            Add a HTTP GET parameter
        :meth:`.Request.fetch`
            Fetch the result.

    Attributes:
        :attr:`.spacegdn`
            The :class:`pyspacegdn.SpaceGDN` instance used to create this
            request

    """

    def __init__(self, spacegdn):
        """ Instantiate a new :class:`.Request`.

        This should only be called by classes, functions or modules in
        `pySpaceGDN`.

        """
        self.spacegdn = spacegdn

        self._headers = dict()
        self._post_params = dict()
        self._get_params = dict()
        self._path = None

        self._headers['User-Agent'] = self.spacegdn.user_agent
        self._headers['Accept'] = 'application/json'

    def set_path(self, path):
        """ Set the path this request will query.

        The path should not start with a forward-slash, unless the resulting
        URL is intended to be `http://endpoint.example//path`.

        Arguments:
            `path`
                The path this request should query

        """
        self._path = path
        return self

    def add_post_param(self, key, value):
        """ Add a HTTP `POST` parameter.

        Arguments:
            `key`
                The key for the parameter
            `value`
                The value of the parameter

        """
        self._post_params[key] = value
        return self

    def add_get_param(self, key, value):
        """ Add a HTTP `GET` parameter.

        Arguments:
            `key`
                The key for the parameter
            `value`
                The value of the parameter

        """
        self._get_params[key] = value
        return self

    def _fetch(self, default_path):
        """ Internal method for fetching.

        This differs from :meth:`.fetch` in that it accepts a default path as
        an argument.

        """
        if not self._path:
            path = default_path
        else:
            path = self._path

        req_type = 'GET' if len(self._post_params) == 0 else 'POST'
        url = '/'.join(['http:/', self.spacegdn.endpoint, path])
        resp = requests.request(req_type, url, params=self._get_params,
                                data=self._post_params, headers=self._headers)
        response = Response()
        data = None
        if resp.ok:
            data = resp.json()
        response.add(data, resp.status_code, resp.reason)

        return response

    def fetch(self):
        """ Execute the request and fetch the result.

        The result will be returned as a :class:`pyspacegdn.Response`
        object.

        """
        return self._fetch(str())
