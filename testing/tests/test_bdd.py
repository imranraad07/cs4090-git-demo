import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pytest_bdd import scenarios, given, when, then
from app.temperature import Temperature

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FEATURE_PATH = os.path.join(BASE_DIR, "features", "temperature.feature")
print(FEATURE_PATH)

scenarios(FEATURE_PATH)
@given("a celsius temperature of 0", target_fixture="temp_obj")
def step_temp():
    return Temperature(0, "C")

@when("converted to fahrenheit")
def convert(temp_obj):
    temp_obj.result = temp_obj.to_fahrenheit()

@then("the result should be 32")
def check(temp_obj):
    assert temp_obj.result == 32

