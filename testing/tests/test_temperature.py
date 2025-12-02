import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.temperature import Temperature
import pytest
def test_convert_c_to_f():
    assert Temperature(0,"C").to_fahrenheit()==32
def test_convert_f_to_c():
    assert Temperature(32,"F").to_celsius()==0
def test_add_same_unit():
    r=Temperature(10,"C")+Temperature(5,"C")
    assert r.value==15 and r.unit=="C"
def test_add_unit_mismatch():
    with pytest.raises(ValueError):
        Temperature(10,"C")+Temperature(50,"F")
