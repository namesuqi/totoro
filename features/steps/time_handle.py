# coding=utf-8
# author: guzehao


import time

from behave import *


@step('wait {number:d} seconds')
def time_sleep(context, number):
    time.sleep(number)


def get_millisecond_now():
    return int(time.time()*1000)

