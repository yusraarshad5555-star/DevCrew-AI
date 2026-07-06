import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_addition(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)

    def test_subtraction(self):
        result = self.calc.subtract(5, 2)
        self.assertEqual(result, 3)

    def test_multiplication(self):
        result = self.calc.multiply(4, 6)
        self.assertEqual(result, 24)

    def test_division(self):
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5.0)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == '__main__':
    unittest.main()