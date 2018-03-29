# coding=utf-8
# author: zengyuetian

from behave import *
from hamcrest import *


@then('response error_code should be {error_code}')
def verify_response_error_code(context, error_code):
    try:
        real_error_code = context.response.json().get('error', 'None')
    except ValueError:
        real_error_code = 'None'
    except AttributeError:
        real_error_code = 'None'

    assert_that(real_error_code, equal_to(error_code),
                "response error code: %s" % real_error_code)


@then('response status_code should be {number}')
def verify_response_status_code(context, number):
    expected_status_code = int(number)
    real_status_code = context.response.status_code
    assert_that(real_status_code, equal_to(expected_status_code),
                "response status code is: %d" % context.response.status_code)


@then('response data should be {data}')
def verify_response_data(context, data):
    if data == "None":
        expected_data = ""
    elif data == 'empty json':
        expected_data = '{}'
    else:
        expected_data = data

    real_data = context.response.text
    assert_that(real_data, equal_to(expected_data),
                "response data is {0}".format(data))


# @then('{field} should be {value}')
# def verify_field_value(context, field, value):
#
#     try:
#         real_value = context.response.json().get(field, None)
#     except Exception as err:
#         # print err.message
#         real_value = None
#
#     except_value = value
#     assert_that(real_value, equal_to(except_value), "{0}'s real value is {1}".format(field, real_value))


# @then('the response data should be \{{field}: {expect}\}')
# def verify_field_value(context, field, expect):
#     try:
#         real_value = context.response.json().get(field, None)
#     except ValueError or TypeError:
#         real_value = context.response
#     assert_that(real_value, equal_to(expect))

