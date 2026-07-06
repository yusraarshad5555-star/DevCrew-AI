import numpy as np

class DoublePrecisionCalculator:
    def __init__(self):
        self.result = 0.0

    def add(self, a: float, b: float) -> None:
        self.result += a + b

    def subtract(self, a: float, b: float) -> None:
        self.result -= a - b

    def multiply(self, a: float, b: float) -> None:
        self.result *= a * b

    def divide(self, a: float, b: float) -> None:
        if b != 0.0:
            self.result /= a / b
        else:
            raise ValueError("Division by zero")

    def clear(self) -> None:
        self.result = 0.0

    def get_result(self) -> float:
        return self.result

# Unit tests for the DoublePrecisionCalculator class
def test_double_precision_calculator():
    calc = DoublePrecisionCalculator()
    
    # Test addition
    calc.add(2.5, 3.5)
    assert np.isclose(calc.get_result(), 6.0), "Addition failed"
    
    # Test subtraction
    calc.subtract(4.0, 1.5)
    assert np.isclose(calc.get_result(), 2.5), "Subtraction failed"
    
    # Test multiplication
    calc.multiply(2.0, 3.0)
    assert np.isclose(calc.get_result(), 6.0), "Multiplication failed"
    
    # Test division
    calc.divide(10.0, 2.0)
    assert np.isclose(calc.get_result(), 5.0), "Division failed"
    
    # Test clear
    calc.clear()
    assert calc.get_result() == 0.0, "Clear operation failed"

# Run the tests
test_double_precision_calculator()