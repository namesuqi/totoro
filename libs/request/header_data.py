"""
HTTP header class

modified by donghao 2016.08.03

"""


class HeaderData(object):

    def __init__(self):
        self._items = {}

    def __getattr__(self, key):
        self._key = key.replace('__', '-')
        return self

    def __call__(self, value):
        if value is not None:
            self._items = dict(self._items.items() + {self._key: value}.items())
        return self

    def __str__(self):
        return str(self._items)

    def __repr__(self):
        return self._items

    def get_res(self):
        return self._items
