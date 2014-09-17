""" Find request for `pySpaceGDN`. """

import requests
from pyspacegdn import Response
from pyspacegdn import FILTER_DELIMITER, ELEMENT_DELIMITER


class FindRequest(object):

    """ A `find` request to SpaceGDN.

    This class represents and builds a `find` request for SpaceGDN. It should
    be used to both create the request, and execute it.

    Methods:
        `type`
            Set the type of elements in the response
        `include_parents`
            Define if the response should contain parent data
        `parents`
            Set parents
        `parent`
            Set a parent, alias for parents
        `sort`
            Define how the results should be sorted
        `where`
            Add filters
        `fetch`
            Send the request to SpaceGDN and fetch the results

    """

    def __init__(self, spacegdn):
        """ Instantiate a new `FindRequest`.

        This method should not be called by anything outside `pySpaceGDN`.

        """
        self.spacegdn = spacegdn

        self._type = None
        self._include_parents = False
        self._parents = list()
        self._sort = None
        self._where = None

    def type(self, return_type):
        """ Set the type the result elements has to be of.

        Arguments:
            `return_type` (`str`)
                The type of elements to get

        """
        self._type = return_type
        return self

    def include_parents(self):
        """ Include parent data in the response.

        This is also called 'bubbling'. See also the documentation on
        `bubbling`_.

        .. _bubbling: https://github.com/XereoNet/SpaceGDN/wiki/API#bubbling

        """
        self._include_parents = True
        return self

    def parents(self, *parents):
        """ Find only elements that are children of these parents.

        The order of the parents matter. In reality only the last parent is
        accounted for.

        Arguments:
            `*parents` (`str`)
                The parents all elements must have

        """
        self._parents += parents
        return self

    # Alias `parents` to `parent`
    parent = parents

    def sort(self, *sort):
        """ Sort the results.

        Define how the results should be sorted. The arguments should be tuples
        of string defining the key and direction to sort by. For example
        `('name', 'asc')` and `('version', 'desc')`. The first sorte rule is
        considered first by the API. See also the API documentation on
        `sorting`_.

        Arguments:
            `*sort` (`tuple`)
                The rules to sort by

        .. _sorting: https://github.com/XereoNet/SpaceGDN/wiki/API#sorting

        """
        self._sort = FILTER_DELIMITER.join(
            [ELEMENT_DELIMITER.join(elements) for elements in sort])
        return self

    def where(self, *where):
        """ Filter the results.

        Filter the results by provided rules. The rules should be dictionaries
        that looks like this::

            {
                '<key>': '<operator>',
                'value': '<value>'
            }

        For example::

            {
                'name': '$eq',
                'value': 'Vanilla Minecraft'
            }

        This is also covered in the documentation_ of the SpaceGDN API.

        .. _documentation: https://github.com/XereoNet/SpaceGDN/wiki/API#where

        """
        filters = list()
        for filter_ in where:
            key = (filter_.keys() - {'value'}).pop()
            operator = filter_[key]
            value = str(filter_['value'])
            filters.append(ELEMENT_DELIMITER.join((key, operator, value)))
        self._where = FILTER_DELIMITER.join(filters)
        return self

    def fetch(self):
        """ Run the request and fetch the results.

        This method will compile the request, send it to the SpaceGDN endpoint
        defined with the `SpaceGDN` object and wrap the results in a `Response`
        object.

        Returns a `Response` object.

        """
        url = '/'.join(['http:/', self.spacegdn.endpoint, 'v2']
                       + self._parents)
        query_args = dict()
        if self._type:
            query_args['r'] = self._type
        if self._include_parents:
            query_args['parents'] = True
        if self._sort:
            query_args['sort'] = self._sort
        if self._where:
            query_args['where'] = self._where

        headers = dict()
        headers['Accept'] = 'application/json'
        headers['User-Agent'] = self.spacegdn.user_agent

        response = Response()
        has_next = True
        while has_next:
            resp = requests.get(url, params=query_args,
                                headers=headers)
            results = None
            if response.success:
                data = resp.json()
                results = data['results']
                query_args['page'] = data['pagination']['page'] + 1
                has_next = data['pagination']['has_next']
            response.add(results, resp.status_code, resp.reason)

        return response
