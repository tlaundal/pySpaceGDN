import unittest
import pyspacegdn
from pyspacegdn import SpaceGDN
from pyspacegdn.requests import Request
from requests.utils import default_user_agent


class SpaceGDNTests(unittest.TestCase):

    def test_basic(self):
        gdn = SpaceGDN()
        self.assertEqual(gdn.endpoint, pyspacegdn.DEFAULT_ENDPOINT)
        self.assertTrue(gdn.user_agent.endswith(
            '{}/{} {}'.format(pyspacegdn.__title__, pyspacegdn.__version__,
                              default_user_agent())))

    def test_user_agent(self):
        name = "N<a>me"
        version = '0.10-beta1'
        gdn = SpaceGDN(name, version)
        self.assertTrue(
            gdn.user_agent.startswith('{}/{}'.format(name, version)))

    def test_requests(self):
        gdn = SpaceGDN()
        self.assertIsInstance(gdn.find(), Request)
        self.assertIsInstance(gdn.usage(), Request)
