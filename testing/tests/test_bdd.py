from pytest_bdd import scenarios, given, when, then
from app.temperature import Temperature
scenarios("features/temperature.feature")
@given("a celsius temperature of 0")
def temp_obj(): return Temperature(0,"C")
@when("converted to fahrenheit")
def convert(temp_obj): temp_obj.result=temp_obj.to_fahrenheit()
@then("the result should be 32")
def check(temp_obj): assert temp_obj.result==32
