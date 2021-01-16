class HTTPRequest(object):
    __slots__ = ('__method', 'url', '__version', 'headers', 'body', 'complete')

    def __init__(self):
        self.headers = {}
        self.body = None
        # Flag to be raised once message is complete
        self.complete = False 

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, data):
        if type(data) == bytes:
            data = data.decode()
        self.__method = data

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, data):
        if type(data) == bytes:
            data = data.decode()
        self.__version = data

    def on_url(self, url:bytes):
        self.url = url.decode()

    def on_header(self, name:bytes, value:bytes):
        # append header to headers dict
        self.headers[name.decode()] = value.decode()

    def on_body(self, body:bytes):
        self.body = body.decode()

    def on_status(self, status:bytes):
        print(status)

    def on_message_complete(self):
        self.complete = True

    def collect_message(self):
        request_line = ' '.join([self.method, self.url, self.version]) + '\r\n'
        header_lines = '\r\n'.join([name + ': ' + self.headers[name] for name in self.headers]) + '\r\n'
        
        if self.body:
            return request_line + header_lines + '\r\n' + self.body
        else:
            return request_line + header_lines + '\r\n'

