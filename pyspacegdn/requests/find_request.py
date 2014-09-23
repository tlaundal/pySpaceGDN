""" Find request for `pySpaceGDN`. """

from pyspacegdn import Response, FILTER_DELIMITER, ELEMENT_DELIMITER
from pyspacegdn.requests import Request


class FindRequest(Request):

    """ A `find` request to SpaceGDN.

    This class represents and builds a `find` request for SpaceGDN. It should
    be used to both create the request, and execute it.

    Methods:
        :meth:`.type`
            Set the type of elements in the response
        :meth:`.include_parents`
            Define if the response should contain parent data
        :meth:`.parents`
            Set parents
        :meth:`.parent`
            Set a parent, alias for parents
        :meth:`.sort`
            Define how the results should be sorted
        :meth:`.where`
            Add filters
        :meth:`.FindRequest.fetch`
            Send the request to SpaceGDN and fetch the results

    """

    def type(self, return_type):
        """ Set the type the result elements has to be of.

        Arguments:
            `return_type` (`str`)
                The type of elements to get

        """
        self.add_get_param('r', return_type)
        return self

    def include_parents(self):
        """ Include parent data in the response.

        This is also called 'bubbling'. See also the documentation on
        `bubbling`_.

        .. _bubbling: https://github.com/XereoNet/SpaceGDN/wiki/API#bubbling

        """
        self.add_get_param('parents', True)
        return self

    def parents(self, *parents):
        """ Find only elements that are children of these parents.

        The order of the parents matter. In reality only the last parent is
        accounted for. This method will override the old parents each time it's
        called.

        Arguments:
            `*parents` (`str`)
                The parents all elements must have

        """
        self.set_path('/'.join(('v2',) + parents))
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
        self.add_get_param('sort', FILTER_DELIMITER.join(
            [ELEMENT_DELIMITER.join(elements) for elements in sort]))
        return self

    def where(self, *where):
        """ Filter the results.

        Filter the results by provided rules. The rules should be tuples that
        look like this::

            ('<key>', '<operator>', '<value>')

        For example::

            ('name', '$eq', 'Vanilla Minecraft')

        This is also covered in the documentation_ of the SpaceGDN API.

        .. _documentation: https://github.com/XereoNet/SpaceGDN/wiki/API#where

        """
        filters = list()
        for key, operator, value in where:
            filters.append(ELEMENT_DELIMITER.join((key, operator, value)))
        self.add_get_param('where', FILTER_DELIMITER.join(filters))
        return self

    def fetch(self):
        """ Run the request and fetch the results.

        This method will compile the request, send it to the SpaceGDN endpoint
        defined with the `SpaceGDN` object and wrap the results in a
        :class:`pyspacegdn.Response` object.

        Returns a :class:`pyspacegdn.Response` object.

        """
        response = Response()
        has_next = True
        while has_next:
            resp = self._fetch(default_path='v2')
            results = None
            if resp.success:
                results = resp.data['results']
                self.add_get_param('page', resp.data['pagination']['page'] + 1)
                has_next = resp.data['pagination']['has_next']
            response.add(results, resp.status_code, resp.status_reason)

        return response
