import unittest
from pyspacegdn import Response


class ResponseTest(unittest.TestCase):

    def test_unloaded(self):
        response = Response()
        self.assertFalse(response.success)

    def test_200OK(self):
        response = Response()
        response.add([200], 200, 'OK')
        self.assertTrue(response.success)
        self.assertIn(200, response.data)

    def test_492RateLimit(self):
        response = Response()
        response.add([200], 200, 'OK')
        response.add([492], 492, 'Rate limit exceeded!')
        self.assertFalse(response.success)
        self.assertIn(492, response.data)

    def test_contents(self):
        response = Response()
        response.add(['ok'], 200, 'OK')
        response.add([42], 200, 'OK')
        self.assertEquals(response.data, ['ok', 42])

    def test_dict(self):
        data = dict()
        response = Response()
        response.add(data, 200, 'OK')
        self.assertIs(response.data, data)
