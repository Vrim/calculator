from calculator import Calculator, Equation


def test_calculate() -> None:
    """Tests all functions in the calculator"""
    c = Calculator()
    e1 = Equation("1+3*4*4+3+5/5")
    e2 = Equation("34*33422-34234+343/343+334-34+2")
    e3 = Equation("3 * (1+2)")
    e4 = Equation("3(1+2)")
    e5 = Equation("3.0 * 2.0")
    e6 = Equation("3^2")
    e7 = Equation("4 % 3")
    assert c.calculate(e1) == 53.0
    assert c.calculate(e2) == 1102417.0
    assert c.calculate(e3) == 9
    assert c.calculate(e4) == 9
    assert c.calculate(e5) == 6.0
    assert c.calculate(e6) == 9
    assert c.calculate(e7) == 1


if __name__ == "__main__":
    import pytest

    pytest.main(['tests.py'])
