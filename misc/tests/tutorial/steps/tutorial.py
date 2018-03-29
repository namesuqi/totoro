from behave import *
import parse
from hamcrest import assert_that, equal_to


@given('we have behave installed')
def step_impl(context):
    pass


@when('we implement a test')
def step_impl(context):
    assert True is not False


@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False


@parse.with_pattern(r"\d+")
def parse_number(text):
    return int(text)


register_type(Number=parse_number)


@given('test params type {number:Number}, {number2}')
def test(context, number, number2):
    assert isinstance(number, int)
    assert isinstance(number2, basestring)
    context.number = number
    context.number2 = number2


@then('assert int {num1:Number}, and string {num2}')
def test2(context, num1, num2):
    assert_that(context.number, equal_to(num1))
    assert_that(context.number2, equal_to(num2))
    pass
