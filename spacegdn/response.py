class Response(object):

    def __init__(self, data=None, status_code=200, status_reason='OK'):
        self.status_code = status_code
        self.status_reason = status_reason
        self.ok = status_code == 200

        if self.ok:
            self.data = data
        else:
            self.data = None

    def add(self, data, status_code, status_reason):
        self.status_code = status_code
        self.status_reason = status_reason
        self.ok = status_code == 200

        if self.ok:
            if not self.data:
                self.data = list()
            self.data += data

    def is_rate_limit_exceeded(self):
        return self.status_code == 492

    def is_malformed_request(self):
        return self.status_code == 400

    def get_status(self):
        return self.status_code, self.status_reason
