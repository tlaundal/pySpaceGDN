import unittest
import mock
from pyspacegdn.requests import FindRequest


class FindRequestTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.path('pyspacegdn.requests.Request')
        self.addCleanup(patcher.stop)
        self.Request = patcher.start()
        self.gdn = mock.MagicMock(name='spacegdn_mock')

        self.request = FindRequest(self.gdn)
