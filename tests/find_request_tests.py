import unittest
from pyspacegdn.requests import FindRequest
from .request_tests import RequestTestBase


class FindRequestTest(RequestTestBase, unittest.TestCase):

    def setUp(self):
        self.setup_base(FindRequest)

    def template(self):
        return {"pagination": {"per_page": 100, "has_next": False,
                               "has_prev": False, "page": 1, "items": 0},
                "results": []}

    def test_type(self):
        self.request.type('game')
        _, call = self.fetch(self.template())
        self.assertIn('r', call[2])
        self.assertEquals('game', call[2]['r'])

    def test_include_parents(self):
        self.request.include_parents()
        _, call = self.fetch(self.template())
        self.assertIn('parents', call[2])

    def test_default_path(self):
        _, call = self.fetch(self.template())
        url = call[1].split('?')[0]
        self.assertTrue(url.endswith('/v2') or url.endswith('/v2/'))

    def test_parents(self):
        self.request.parents('game/distribution')
        _, call = self.fetch(self.template())
        url = call[1].split('?')[0]
        self.assertTrue(url.endswith('/v2/game/distribution') or
                        url.endswith('/v2/game/distribution/'))

    def test_sort(self):
        self.request.sort(('key1', 'asc'), ('key2', 'desc'), ('key3', 'desc'))
        _, call = self.fetch(self.template())
        self.assertIn('sort', call[2])
        self.assertEqual('key1.asc|key2.desc|key3.desc', call[2]['sort'])

    def test_where(self):
        self.request.where(('key1', '$eq', 'value1'),
                           ('key2', '$lt', 'value2'))
        _, call = self.fetch(self.template())
        self.assertIn('where', call[2])
        self.assertEqual('key1.$eq.value1|key2.$lt.value2', call[2]['where'])
