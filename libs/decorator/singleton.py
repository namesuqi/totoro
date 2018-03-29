# coding=utf-8
"""
单例装饰器

__author__ = 'zengyuetian'

单例类本身不会知道自己是单例，因为他本身并不是单例的
"""


def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton()