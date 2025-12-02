import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.stack import Stack
import pytest
def test_push_and_pop():
    s=Stack(); s.push(10); assert s.pop()==10
def test_empty_pop():
    with pytest.raises(IndexError): Stack().pop()
