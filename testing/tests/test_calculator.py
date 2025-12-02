import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.calculator import add, divide, square
import pytest
def test_add_basic(): 
    assert add(2,3)==5

def test_divide_success(): 
    assert divide(10,2)==5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError): 
        divide(5,0)

@pytest.mark.parametrize("x,result",[(-3,9),(0,0),(4,16)])
def test_square_param(x,result): 
    assert square(x)==result
