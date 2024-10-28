import pytest
from src.utils.price_utils import clean_price

def test_unit_prices():
    """Test the cleaning of unit prices."""
    assert clean_price("2                     €                    ,89") == 2.89
    assert clean_price("9                     €                    ,39") == 9.39
    assert clean_price("10                    €                    ,00") == 10.0
    assert clean_price("") is None
    assert clean_price(None) is None

def test_kilogram_prices():
    """Test the cleaning of kilogram prices."""
    assert clean_price("55,58 € / kg") == 55.58
    assert clean_price("49,42 € / kg") == 49.42
    assert clean_price("18,01 € / kg") == 18.01

def test_invalid_prices():
    """Test the handling of invalid prices."""
    assert clean_price("abc") is None
    assert clean_price("€") is None
    assert clean_price("1,2,3") is None
    assert clean_price("1.2.3") is None