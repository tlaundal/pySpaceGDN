import unittest
import mock
from pyspacegdn.requests import Request


class RequestTestBase(object):

    request_type = None
    request = None
    gdn = None
    _params = None

    def setup_base(self, request):
        self.gdn = mock.MagicMock(name='Spacegdn')
        self.gdn.client_name = 'Mocked SpaceGDN'
        self.gdn.client_version = '1.0'
        self.gdn.endpoint = 'endpoint.example'
        self.gdn.user_agent = 'Mocked-SpaceGDN/1.0'

        self.request_type = request
        self.request = self.request_type(self.gdn)

    def fetch(self, result_data=None, status_code=200, status_reason='OK'):
        """ Excecute a mocked fetch on the `self.request` object.

        Arguments:
            result_data - The data that should be returned from requets.request
            status_code=200
            status_reason='OK'

        A two-tuple is returned. The first value is the response from the
        Request.fetch call, and the other it a tuple of the arguments sent to
        requests.request."""

        if not result_data:
            result_data = list()

        def fake_request(proto, url, params=None, data=None, headers=None,
                         **kwargs):
            self._params = (proto, url, params, data, headers, kwargs)
            response = mock.MagicMock(name='requests.Response_mock')
            response.ok = True
            response.status_code = status_code
            response.reason = status_reason
            response.json.return_value = result_data
            return response

        with mock.patch('requests.request', fake_request):
            response = self.request.fetch(), self._params
            self._params = None
            self.request = self.request_type(self.gdn)
            return response


class RequestTest(RequestTestBase, unittest.TestCase):

    def setUp(self):
        self.setup_base(Request)

    def test_headers(self):
        _, call = self.fetch()
        headers = call[4]
        self.assertIn('Accept', headers)
        self.assertIn('User-Agent', headers)
        self.assertEqual('application/json', headers['Accept'])
        self.assertEqual(self.gdn.user_agent, headers['User-Agent'])

    def check_protocol(self, proto, data):
        response, call = self.fetch(data)
        self.assertEqual(proto, call[0])
        return response, call

    def check_path(self, expected, data):
        response, call = self.fetch(data)
        self.assertEqual('http://'+self.gdn.endpoint+'/'+expected,
                         call[1])
        return response, call

    def test_protocol_default(self):
        """ Test that the default protocol is GET. """
        self.check_protocol('GET', [])

    def test_protocol_get(self):
        """ Test that the protocol when using only params is GET. """
        self.request.add_get_param('key', 'value')
        self.check_protocol('GET', [])

    def test_protocol_post_only(self):
        self.request.add_post_param('key', 'value')
        self.check_protocol('POST', [])

    def test_protocol_post_both(self):
        self.request.add_get_param('key', 'value')
        self.request.add_post_param('key', 'value')
        self.check_protocol('POST', [])

    def test_path_plain(self):
        self.check_path('', [])

    def test_path_normal(self):
        self.request.set_path('test1/')
        self.check_path('test1/', [])

    def test_get_parameters(self):
        params = {
            'key1': 'value',
            'key2': 42,
            'key3': True,
            4: 'value4'
        }
        for key, value in params.items():
            self.request.add_get_param(key, value)
        _, call = self.fetch()
        for key, value in params.items():
            self.assertIn(key, call[2])
            self.assertEqual(value, call[2][key])

    def test_post_parameters(self):
        params = {
            'key1': 'value',
            'key2': 42,
            'key3': True,
            4: 'value4'
        }
        for key, value in params.items():
            self.request.add_post_param(key, value)
        _, call = self.fetch()
        for key, value in params.items():
            self.assertIn(key, call[3])
            self.assertEqual(value, call[3][key])
