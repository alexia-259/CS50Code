from twttr import shorten

def test_twttr_lower():
    assert shorten("weeew2") == "ww2"

def test_twttr_upper():
    assert shorten("WEEEW!") == "WW!"




