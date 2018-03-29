# coding=utf-8

"""
__author__ = 'zengyuetian'
precondition: pip install redis
modified by dh 2015.08.11
"""

import redis


class RedisDB(object):
    def connect(self, host='127.0.0.1', port=6379, db=0):
        self._db = redis.Redis(host=host, port=port, db=db)

    def shutdown(self):
        self._db.shutdown()

    def select_db(self, db):
        self._db.select(db)

    def remove_db(self, db):
        self._db.move(db)

    def set(self, key, value):
        self._db.set(key, value)

    def get(self, key):
        return self._db.get(key)

    def get_keys(self):
        return self._db.keys()

    def llen(self, key):
        return self._db.llen(key)


if __name__ == "__main__":
    pass
