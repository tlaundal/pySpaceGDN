""" Response class for `pySpaceGDN`. """


class Response(object):

    """ A response from SpaceGDN.

    This class defines a response from the SpaceGDN API. It may represent both
    erroneous and successful responses from the API. Some convenience methods
    and fields are defined for easy analysis of the response.

    This class is intended to be instantiated from `pySpaceGDN`, and not by an
    application  using the framework. The `Response` object will then be
    populated by `pySpaceGDN`, with pages from SpaceGDN. The status of the
    response is given by the last page got from SpaceGDN. If a page fails, no
    other pages will be loaded. When the response object is fully populated,
    it can be used by other classes.

    When a `Response` object is first instantiated, `status_code`,
    `status_reason` and `ok` is set to `0`, `'Not loaded'` and `False`,
    respectively.

    Methods:
        add                    -- For adding pages, only for internal use
        is_rate_limit_exceeded -- Check if error was exceeded rate limit
        is_malformed_request   -- Check if error was malformed request

    Attributes:
        status_code   -- The raw HTTP status code, for example 200
        status_reason -- The reason or description for the status, for example
                         OK
        ok            -- Whether the response is OK/successful. This is just a
                         check as to whether status_code is 200
        data          -- The data in the response, typically a list or
                         dictionary

    """

    data = None
    status_code = 0
    status_reason = 'Not loaded'
    ok = False

    def add(self, data, status_code, status_reason):
        """ Add data to this response.

        This method should be used to add data to the response. The data should
        be all the data returned in one page from SpaceGDN.

        If this method is called before, data will be appended to the existing
        data with `+=`, this means dicts, for instance will not work with
        multiple pages.

        Arguments:
            data          -- The data to add
            status_code   -- The HTTP response code of the HTTP response
                             containing the data
            status_reason -- The reason or description for the HTTP response
                             code

        """
        self.status_code = status_code
        self.status_reason = status_reason

        self.ok = status_code == 200

        if self.ok:
            if not self.data:
                self.data = list()
            self.data += data

    def is_rate_limit_exceeded(self):
        """ Check whether the response is a 'rate limit exceeded' response. """
        return self.status_code == 492

    def is_malformed_request(self):
        """ Check whether the response is a 'malformed request' response. """
        return self.status_code == 400
