import json

from tornado.web import asynchronous

from apphandler.application import Loadable


class JsonRESTExample(Loadable):

    @asynchronous
    def get(self, *args, **kwargs):
        result = {"data": "some data"}
        self.write(json.dumps(result))
        self.finish()

