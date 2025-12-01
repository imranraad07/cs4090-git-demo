from hypothesis import given
import hypothesis.strategies as st
from app.calculator import add, square
@given(st.integers(), st.integers())
def test_add_commutative(a,b): assert add(a,b)==add(b,a)
@given(st.integers())
def test_square_non_negative(x): assert square(x)>=0
