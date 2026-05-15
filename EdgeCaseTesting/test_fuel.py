from fuel import convert, gauge
import pytest

def test_value_converter():
    assert convert("3/4") == 75
    assert convert("0/4") == 0
    assert convert("4/4") == 100

def test_Erorrs_converter():
    with pytest.raises(ValueError):
        convert("three/four")
    with pytest.raises(ValueError):
        convert("-5/3")
    with pytest.raises(ZeroDivisionError):
        convert("4/0")



def test_gauge_():
    assert gauge(75) == "75%"
    assert gauge(99) == "F"
    assert gauge(1) == "E"



