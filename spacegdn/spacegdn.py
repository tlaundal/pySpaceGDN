import requests
import spacegdn
from spacegdn.requests import FindRequest


class SpaceGDN(object):

    def __init__(self, client_name=None, client_version=None,
                 endpoint=spacegdn.DEFAULT_ENDPOINT):
        self.client_name = client_name
        self.client_version = client_version
        self.endpoint = endpoint

        self.user_agent = '{}/{} {}'.format(
            spacegdn.name, spacegdn.version,
            requests.utils.default_user_agent())
        if client_name:
            self.user_agent = '{}/{} {}'.format(
                self.client_name, self.client_version,
                self.user_agent)

    def find(self):
        return FindRequest(self)
