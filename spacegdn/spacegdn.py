import requests
import spacegdn
from spacegdn.requests import FindRequest


class SpaceGDN(object):

    def __init__(self, client_name='Uknown', client_version='uknown',
                 endpoint=spacegdn.DEFAULT_ENDPOINT):
        self.client_name = client_name
        self.client_version = client_version
        self.endpoint = endpoint

        self.user_agent = '{}/{} {}/{} {}'.format(
            self.client_name, self.client_version,
            spacegdn.name, spacegdn.version,
            requests.utils.default_user_agent())

    def find(self):
        return FindRequest(self)
