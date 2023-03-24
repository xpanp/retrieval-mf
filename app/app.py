from datetime import date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.utils.error_type import ServerError

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()

class Flask(_Flask):
    json_encoder = JSONEncoder

    def set_cfg(self, cfg):
        self.cfg = cfg

    def start(self):
        self.run(host=self.cfg.HOST, port=self.cfg.PORT, debug=self.cfg.DEBUG)
