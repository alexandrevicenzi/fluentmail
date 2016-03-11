# -*- coding: utf-8 -*-


class BaseBackend(object):

    def open(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def send(self, message):
        if isinstance(message, (list, tuple)):
            self.send_multiple(message)
        else:
            self.send_multiple([message])

    def send_multiple(self, messages):
        pass
