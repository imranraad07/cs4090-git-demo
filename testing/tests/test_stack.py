from app.stack import Stack
import pytest
def test_push_and_pop():
    s=Stack(); s.push(10); assert s.pop()==10
def test_empty_pop():
    with pytest.raises(IndexError): Stack().pop()
