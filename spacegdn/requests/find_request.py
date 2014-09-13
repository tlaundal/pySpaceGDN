import requests
from spacegdn import Response
from spacegdn import FILTER_DELIMITER, ELEMENT_DELIMITER


class FindRequest(object):

    def __init__(self, spacegdn):
        self.spacegdn = spacegdn

        self._type = None
        self._include_parents = False
        self._parents = list()
        self._sort = None
        self._where = None

    def type(self, return_type):
        self._type = return_type
        return self

    def include_parents(self):
        self._include_parents = True
        return self

    def parents(self, *parents):
        self._parents += parents
        return self

    def parent(self, parent):
        self._parents += parent
        return self

    def sort(self, *sort):
        self._sort = FILTER_DELIMITER.join(
            [ELEMENT_DELIMITER.join(elements) for elements in sort])
        return self

    def where(self, *where):
        filters = list()
        for f in where:
            key = (f.keys() - {'value'}).pop()
            operator = f[key]
            value = str(f['value'])
            filters.append(ELEMENT_DELIMITER.join((key, operator, value)))
        self._where = FILTER_DELIMITER.join(filters)
        return self

    def fetch(self):
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
            if (response.ok):
                data = resp.json()
                results = data['results']
                query_args['page'] = data['pagination']['page'] + 1
                has_next = data['pagination']['has_next']
            response.add(results, resp.status_code, resp.reason)

        return response
