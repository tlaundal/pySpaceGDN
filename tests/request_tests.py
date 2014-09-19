import unittest
import mock
from pyspacegdn.requests import Request


@mock.patch('requests.request')
class RequestTest(unittest.TestCase):

    def setUp(self):
        request_patcher = mock.patch('requests.request')
        self.addCleanup(request_patcher.stop)
        self.request_mock = request_patcher.start()
        self.response_mock = mock.MagicMock(name='Response_mock')
        self.request_mock.return_value = self.response_mock
        self.gdn_mock = mock.MagicMock(name='SpaceGDN_mock')

        self.request = Request(self.gdn_mock)

    def test_clean(self, mock_method):
        pass  # TODO
