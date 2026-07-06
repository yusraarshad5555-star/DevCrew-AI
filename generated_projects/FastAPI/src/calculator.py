class Calculator:
    """A robust, production-quality offline calculator implementation."""
    
    def add(self, a: float, b: float) -> float:
        return float(a + b)
        
    def subtract(self, a: float, b: float) -> float:
        return float(a - b)
        
    def multiply(self, a: float, b: float) -> float:
        return float(a * b)
        
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return float(a / b)
        
    def power(self, base: float, exponent: float) -> float:
        return float(base ** exponent)